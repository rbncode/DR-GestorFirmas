import { Ionicons } from '@expo/vector-icons';
import { Picker } from '@react-native-picker/picker';
import * as DocumentPicker from 'expo-document-picker';
import React, { useState } from 'react';
import {
  Alert,
  Modal,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View
} from 'react-native';

export default function UploadFileEmpleado() {
  const [supervisor, setSupervisor] = useState<string>('');
  const [tipoSolicitud, setTipoSolicitud] = useState<string>('');
  const [titulo, setTitulo] = useState<string>('');
  const [descripcion, setDescripcion] = useState<string>('');
  const [modalVisible, setModalVisible] = useState<boolean>(false);
  const [confirmModalVisible, setConfirmModalVisible] = useState<boolean>(false);

  const [selectedFile, setSelectedFile] = useState<DocumentPicker.DocumentPickerResult | null>(null);

  const handleSelectFile = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: 'application/pdf',
        copyToCacheDirectory: true,
      });

      if (!result.canceled && result.assets && result.assets.length > 0) {
        setSelectedFile(result);
        setModalVisible(false);
      }
    } catch (error) {
      console.error(error);
      Alert.alert('Error', 'No se pudo seleccionar el archivo');
    }
  };

  const handleSubmit = async () => {
    if (!supervisor || !tipoSolicitud || !titulo || !descripcion || !selectedFile) {
      Alert.alert('Error', 'Por favor completa todos los campos y sube el archivo');
      return;
    }

    try {
      // 1. Crear la solicitud
      const solicitudBody = {
        titulo,
        categoria: tipoSolicitud,
        descripcion,
        fecha: new Date().toISOString(),
        empleado: {
          nombre: "Empleado Ejemplo",
          correo: "empleado@ejemplo.com",
          rol: "empleado"
        },
        supervisor: {
          nombre: supervisor,
          correo: "supervisor@ejemplo.com",
          rol: "supervisor"
        },
        hr: {
          nombre: "RH",
          correo: "rh@ejemplo.com",
          rol: "hr"
        },
        documentoId: ""
      };

      console.log('Enviando solicitud:', JSON.stringify(solicitudBody, null, 2));

      const solicitudRes = await fetch('http://localhost:8080/api/solicitudes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(solicitudBody)
      });

      if (!solicitudRes.ok) {
        const errorText = await solicitudRes.text();
        console.error('Error al crear solicitud:', errorText);
        throw new Error(`Error al crear la solicitud: ${solicitudRes.status}`);
      }

      const solicitud = await solicitudRes.json();
      console.log('Solicitud creada:', solicitud);

      // 2. Subir el archivo PDF
      const fileAsset = selectedFile.assets[0];
      const file = await fetch(fileAsset.uri);
      const blob = await file.blob();

      const formData = new FormData();
      formData.append('solicitud_id', solicitud.id);
      formData.append('filename', fileAsset.name);
      formData.append('file', blob, fileAsset.name);

      const uploadRes = await fetch('http://localhost:8080/api/agregarPDF', {
        method: 'POST',
        body: formData,
      });

      if (!uploadRes.ok) {
        const errorText = await uploadRes.text();
        console.error('Error subiendo archivo:', errorText);
        throw new Error(`Error al subir el archivo: ${uploadRes.status}`);
      }

      console.log('Archivo subido correctamente');
      setConfirmModalVisible(true);
    } catch (error) {
      console.error('Error al enviar:', error);
      Alert.alert('Error', 'Hubo un problema al enviar la solicitud');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Subir Solicitud</Text>

      <TextInput
        style={styles.input}
        placeholder="Nombre del Supervisor"
        value={supervisor}
        onChangeText={setSupervisor}
      />

      <Picker
        selectedValue={tipoSolicitud}
        onValueChange={(itemValue) => setTipoSolicitud(itemValue)}
        style={styles.picker}
      >
        <Picker.Item label="Selecciona un tipo de solicitud" value="" />
        <Picker.Item label="Vacaciones" value="vacaciones" />
        <Picker.Item label="Permiso" value="permiso" />
        <Picker.Item label="Otro" value="otro" />
      </Picker>

      <TextInput
        style={styles.input}
        placeholder="Título"
        value={titulo}
        onChangeText={setTitulo}
      />

      <TextInput
        style={[styles.input, styles.textArea]}
        placeholder="Descripción"
        value={descripcion}
        onChangeText={setDescripcion}
        multiline
        numberOfLines={4}
      />

      <TouchableOpacity onPress={() => setModalVisible(true)} style={styles.fileButton}>
        <Ionicons name="attach" size={24} color="white" />
        <Text style={styles.fileButtonText}>
          {selectedFile ? selectedFile.assets[0].name : 'Seleccionar archivo PDF'}
        </Text>
      </TouchableOpacity>

      <TouchableOpacity onPress={handleSubmit} style={styles.submitButton}>
        <Text style={styles.submitButtonText}>Enviar Solicitud</Text>
      </TouchableOpacity>

      {/* Modal de selección de archivo */}
      <Modal visible={modalVisible} transparent animationType="slide">
        <View style={styles.modalContainer}>
          <TouchableOpacity onPress={handleSelectFile} style={styles.modalButton}>
            <Text style={styles.modalButtonText}>Seleccionar PDF</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={() => setModalVisible(false)} style={styles.modalButton}>
            <Text style={styles.modalButtonText}>Cancelar</Text>
          </TouchableOpacity>
        </View>
      </Modal>

      {/* Modal de confirmación */}
      <Modal visible={confirmModalVisible} transparent animationType="slide">
        <View style={styles.modalContainer}>
          <Text style={styles.confirmText}>¡Solicitud enviada con éxito!</Text>
          <TouchableOpacity onPress={() => setConfirmModalVisible(false)} style={styles.modalButton}>
            <Text style={styles.modalButtonText}>Cerrar</Text>
          </TouchableOpacity>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20, flex: 1, backgroundColor: '#fff' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  input: { borderWidth: 1, borderColor: '#ccc', padding: 10, marginBottom: 15, borderRadius: 5 },
  textArea: { height: 100 },
  picker: { marginBottom: 15 },
  fileButton: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#007AFF', padding: 10, borderRadius: 5, marginBottom: 20 },
  fileButtonText: { color: 'white', marginLeft: 10 },
  submitButton: { backgroundColor: '#28A745', padding: 15, borderRadius: 5 },
  submitButtonText: { color: 'white', textAlign: 'center', fontWeight: 'bold' },
  modalContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: 'rgba(0,0,0,0.5)' },
  modalButton: { backgroundColor: '#fff', padding: 15, borderRadius: 5, marginTop: 10 },
  modalButtonText: { color: '#007AFF', fontWeight: 'bold' },
  confirmText: { backgroundColor: '#fff', padding: 20, fontSize: 18, borderRadius: 5 },
});
