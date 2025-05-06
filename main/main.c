#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <freertos/FreeRTOS.h>
#include "./Funciones/FuncionesNT.h"
#include "./Comunicacion/Comunicaciones.h"
#include "time.h"

#include "cosas.h"

#define TIMEPO_ENTRE_MUESTREO 900 //Segundos
#define DIRECCION_BROKER "mqtt://192.168.18.17:1883"

void app_main(void)
{   
    // Configuración de la hora actual
    time_t tiempo_actual = time(NULL);

    // Configuración de Wi-Fi
    Wifi_config_t wifi_config = {
        .ssid = nombrewifi,
        .password = contrasena
    };
    // Configuración de MQTT
    mqtt_config_t mqtt_config = {
        .uri = DIRECCION_BROKER,
        .client_id = "NT_1",
        .username = "",
        .password = "",
        .topic = "PR2/A9/NT"
    };

    //Variables Main
    uint8_t bateria = 0;
    int8_t temperatura = 0;
    uint8_t humedad = 0;
    error_code_t status = NoError;
    char *json_string = NULL;

    uint8_t intentos = 0;
    const uint8_t max_intentos = 20;

    esp_sleep_wakeup_cause_t causa = esp_sleep_get_wakeup_cause();

    if(!status){status = Init_pin_funcion();}
    if(!status){status = Enable_wifi(&wifi_config);}//funciona
    
    //Espera a la correcta inicializacion del cliente Wi-Fi
    while (!wifi_ready) {
        vTaskDelay(pdMS_TO_TICKS(1000));
        intentos++;
        if (intentos >= max_intentos) {
            ESP_LOGE("WIFI", "No se pudo conectar a la red Wi-Fi en el tiempo esperado");
            status = WiFiError;
            break;
        }
        ESP_LOGI("WIFI", "Esperando a que Wi-Fi esté listo... Intento %d", intentos);
    }

    if(!status){status = mqtt_connect(&mqtt_config);}//Por testar
    if(!status){status = get_data(&temperatura, &humedad, &bateria);}//funciona temperatura y humedad comprobar bateria
    if(!status){status = mqtt_create_json(temperatura, humedad, bateria, &json_string);}//Funciona
    
    //Espera a la correcta inicializacion del cliente MQTT
    while (!mqtt_ready) {
        vTaskDelay(pdMS_TO_TICKS(1000));
        intentos++;
        if (intentos >= max_intentos) {
            ESP_LOGE("MQTT", "No se pudo conectar al broker MQTT en el tiempo esperado");
            status = MQTTError;
            break;
        }
        ESP_LOGI("MQTT", "Esperando a que MQTT esté listo... Intento %d", intentos);
    }
    
    if(!status){status = mqtt_publish(&mqtt_config, mqtt_config.topic, json_string, 0);}
    if (json_string){free(json_string);}//funciona
    ESP_LOGI("Iniciando apagado--------------------------------------","");
    Disable_wifi();
    mqtt_disconnect();

    if (status || causa != ESP_SLEEP_WAKEUP_TIMER){//Solo muestra leds si no es un reinicio por timer o hay error
        ESP_LOGI("Estado", "Estado: %d", status);
        if (status == NoError) {status = 0;}//funciona
        else {status = 1;
    }
    
    Show_status_led(status);}//funciona
    ESP_LOGI("wakeup", "Wakeup cause: %d", causa);
    ESP_LOGI("error", "Error: %d", status);
    if(!status){status = Deep_sleep(((TIMEPO_ENTRE_MUESTREO)-(time(NULL)-tiempo_actual))*1000);}//funciona
    else{Deep_sleep(1000);}//en caso de erro se reinicia
}