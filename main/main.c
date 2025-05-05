#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <freertos/FreeRTOS.h>
#include "./Funciones/FuncionesNT.h"
#include "./Comunicacion/Comunicaciones.h"

#include "cosas.h"


void app_main(void)
{   

    // Configuración de Wi-Fi
    Wifi_config_t wifi_config = {
        .ssid = nombrewifi,
        .password = contrasena
    };
    // Configuración de MQTT
    mqtt_config_t mqtt_config = {
        .broker = "100.93.177.37:1883",
        .client_id = "NT_1",
        .username = "user",
        .password = "password",
        .topic = "NT"
    };

    uint8_t bateria = 0;
    int8_t temperatura = 0;
    uint8_t humedad = 0;
    error_code_t status = NoError;
    char *json_string = NULL;

    if(!status){status = Init_pin_funcion();}
    if(!status){status = Enable_wifi(&wifi_config);}//funciona
    //if(!status){status = mqtt_connect(&mqtt_config);}//Por testar
    if(!status){status = get_data(&temperatura, &humedad, &bateria);}//funciona temperatura y humedad comprobar bateria
    if(!status){status = mqtt_create_json(temperatura, humedad, bateria, &json_string);}//Funciona
    if(!status){status = mqtt_publish(&mqtt_config, mqtt_config.topic, json_string, 0);}
    free(json_string);//funciona

    ESP_LOGI("Iniciando apagado--------------------", "--------------------");
    Disable_wifi();//funciona
    mqtt_disconnect();
    Show_status_led(status);//funciona
    ESP_LOGI("error", "Error: %d", status);
    if(!status){status = Deep_sleep(5000);}//funciona
    
    Deep_sleep(1000);
}