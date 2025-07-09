import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Modal, TextInput, ScrollView, Platform } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { WebView } from 'react-native-webview';

export default function RevisarSolicitud() {
  const router = useRouter();
  const { id } = useLocalSearchParams();

  const solicitud = {
    id: id,
    nombreEmpleado: 'Juanito Perez',
    titulo: 'Vacaciones',
    descripcion: 'Vacaciones de invierno por 10 días',
    fecha: '2024-07-01',
    categoria: 'Vacaciones',
    archivo: 'https://www.unaula.edu.co/sites/default/files/ebooks/ElPrimerAmor.pdf',
    supervisor: 'Carlos Ruiz'
  };

  const [modalVisible, setModalVisible] = useState(false);
  const [motivoRechazo, setMotivoRechazo] = useState('');

  const aceptarSolicitud = () => {
    console.log(`Solicitud ${solicitud.id} aceptada`);
    router.back();
  };

  const rechazarSolicitud = () => {
    setModalVisible(true);
  };

  const confirmarRechazo = () => {
    console.log(`Solicitud ${solicitud.id} rechazada con motivo: ${motivoRechazo}`);
    setModalVisible(false);
    router.back();
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>
        Archivo: {solicitud.titulo} de {solicitud.nombreEmpleado}
      </Text>

      <View style={styles.content}>
        <View style={styles.pdfContainer}>
          {Platform.OS === 'web' ? (
            <iframe
              src={solicitud.archivo}
              style={{ width: '100%', height: '100%' }}
              title="Visor PDF"
            />
          ) : (
            <WebView
              source={{ uri: solicitud.archivo }}
              style={styles.webview}
            />
          )}
        </View>

        <ScrollView style={styles.detailsContainer}>
          <Text style={styles.detailsTitle}>Detalle de la Solicitud</Text>
          <Text>Nombre Empleado: {solicitud.nombreEmpleado}</Text>
          <Text>Nombre Supervisor: {solicitud.supervisor}</Text>
          <Text>Título: {solicitud.titulo}</Text>
          <Text>Descripción: {solicitud.descripcion}</Text>
          <Text>Fecha: {solicitud.fecha}</Text>
          <Text>Categoría: {solicitud.categoria}</Text>

          <TouchableOpacity style={styles.acceptButton} onPress={aceptarSolicitud}>
            <Text style={styles.buttonText}>Aceptar</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.rejectButton} onPress={rechazarSolicitud}>
            <Text style={styles.buttonText}>Rechazar</Text>
          </TouchableOpacity>
        </ScrollView>
      </View>

      <Modal
        visible={modalVisible}
        animationType="slide"
        transparent={true}
      >
        <View style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <Text>Indique el motivo de rechazo:</Text>
            <TextInput
              style={styles.input}
              placeholder="Motivo"
              value={motivoRechazo}
              onChangeText={setMotivoRechazo}
            />
            <TouchableOpacity style={styles.acceptButton} onPress={confirmarRechazo}>
              <Text style={styles.buttonText}>Confirmar rechazo</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.rejectButton} onPress={() => setModalVisible(false)}>
              <Text style={styles.buttonText}>Cancelar</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  header: { fontSize: 18, fontWeight: 'bold', margin: 12, textAlign: 'center' },
  content: { flexDirection: 'row', flex: 1 },
  pdfContainer: { flex: 2, backgroundColor: '#eee' },
  webview: { flex: 1 },
  detailsContainer: { flex: 1, backgroundColor: '#f9f9f9', padding: 10 },
  detailsTitle: { fontSize: 16, fontWeight: 'bold', marginBottom: 8 },
  acceptButton: { backgroundColor: '#4CAF50', padding: 10, borderRadius: 6, marginTop: 10 },
  rejectButton: { backgroundColor: '#e53935', padding: 10, borderRadius: 6, marginTop: 10 },
  buttonText: { color: '#fff', textAlign: 'center' },
  modalContainer: { flex:1, backgroundColor:'rgba(0,0,0,0.5)', justifyContent:'center', alignItems:'center' },
  modalContent: { backgroundColor:'#fff', padding:20, borderRadius:8, width:'80%' },
  input: { borderWidth:1, borderColor:'#ccc', borderRadius:4, padding:8, marginTop:10 }
});
