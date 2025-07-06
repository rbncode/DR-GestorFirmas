import React from 'react';
import { Alert, Button } from 'react-native';

export default function AgregarItemBoton() {
  const agregarUsuario = async () => {
    try {
        await fetch('http://localhost:8080/api/agregarUsuarios', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          correo: 'usuario@ejemplo.com',
          nombre: 'Usuario Prueba',
          contraseña: '123456',
          rol: 'empleado',
        }),
    });
    } catch (error) {
      Alert.alert('Ocurrió un error al conectar con la base');
    }
  };

  return (
    <Button title="Agregar Usuario" onPress={agregarUsuario} />
  );
}