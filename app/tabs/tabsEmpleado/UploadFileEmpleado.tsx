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
      // 1. Crear la solicitud sin documentoId primero
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
        documentoId: "" // Dejarlo vacío inicialmente
      };
    
      console.log('Enviando solicitud:', JSON.stringify(solicitudBody, null, 2));
    
      const solicitudRes = await fetch('http://localhost:8080/api/solicitudes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(solicitudBody)
      });
    
      if (!solicitudRes.ok) {
        const errorText = await solicitudRes.text();
        console.error('Error response:', errorText);
        throw new Error(`Error al crear la solicitud: ${solicitudRes.status}`);
      }
    
      const solicitud = await solicitudRes.json();
      console.log('Solicitud creada:', solicitud);
    
      // 2. Subir el archivo PDF
      const fileAsset = selectedFile.assets[0];
      const formData = new FormData();
      formData.append('solicitud_id', solicitud.id);
      formData.append('filename', fileAsset.name);
      formData.append('file', {
        uri: fileAsset.uri,
        name: fileAsset.name,
        type: 'application/pdf'
      } as any);

      console.log(solicitud.id)
      console.log(fileAsset.name)
      console.log({
        uri: fileAsset.uri,
        name: fileAsset.name,
        type: 'application/pdf'
      } as any)

      const uploadRes = await fetch('http://localhost:8080/api/agregarPDF', {
        method: 'POST',
        body: formData // NO incluir Content-Type header para multipart
      });
    
      if (!uploadRes.ok) {
        const errorText = await uploadRes.text();
        console.error('Error uploading file:', errorText);
        throw new Error(`Error al subir el PDF: ${uploadRes.status}`);
      }
    
      console.log('Archivo subido exitosamente');
      setConfirmModalVisible(true);
      
      // Limpiar el formulario
      setSupervisor('');
      setTipoSolicitud('');
      setTitulo('');
      setDescripcion('');
      setSelectedFile(null);
      
    } catch (error) {
      console.error('Error completo:', error);
      Alert.alert('Error', error.message || 'No se pudo enviar la solicitud');
    }
  };

  const handleConfirm = () => {
    setConfirmModalVisible(false);
    // Aquí podrías navegar con router.push('/home') si usas expo-router
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Subir Solicitud de Empleado</Text>

      {/* Supervisor */}
      <Text style={styles.label}>Supervisor:</Text>
      <View style={styles.pickerContainer}>
        <Picker
          selectedValue={supervisor}
          onValueChange={setSupervisor}
        >
          <Picker.Item label="Seleccionar..." value="" />
          <Picker.Item label="Carlos Ruiz" value="Carlos Ruiz" />
          <Picker.Item label="Ana Gómez" value="Ana Gómez" />
        </Picker>
      </View>

      {/* Tipo solicitud */}
      <Text style={styles.label}>Tipo de Solicitud:</Text>
      <View style={styles.pickerContainer}>
        <Picker
          selectedValue={tipoSolicitud}
          onValueChange={setTipoSolicitud}
        >
          <Picker.Item label="Seleccionar..." value="" />
          <Picker.Item label="Vacaciones" value="Vacaciones" />
          <Picker.Item label="Licencia" value="Licencia" />
        </Picker>
      </View>

      {/* Título */}
      <Text style={styles.label}>Título:</Text>
      <TextInput
        style={styles.input}
        placeholder="Ingrese el título"
        value={titulo}
        onChangeText={setTitulo}
      />

      {/* Descripción */}
      <Text style={styles.label}>Descripción:</Text>
      <TextInput
        style={[styles.input, { height: 100 }]}
        placeholder="Ingrese la descripción"
        multiline
        value={descripcion}
        onChangeText={setDescripcion}
      />

      {/* Botón subir archivo */}
      <TouchableOpacity style={styles.button} onPress={() => setModalVisible(true)}>
        <Text style={styles.buttonText}>Subir Documento</Text>
      </TouchableOpacity>

      {/* Mostrar archivo seleccionado */}
      {selectedFile &&
        selectedFile.assets &&
        selectedFile.assets.length > 0 && (
          <View style={styles.fileInfo}>
            <Ionicons name="document" size={24} color="red" />
            <Text style={{ marginLeft: 8 }}>
              {selectedFile.assets[0].name}
            </Text>
          </View>
      )}

      {/* Botón enviar */}
      <TouchableOpacity style={styles.button} onPress={handleSubmit}>
        <Text style={styles.buttonText}>Enviar Solicitud</Text>
      </TouchableOpacity>

      {/* Modal para subir archivo */}
      <Modal visible={modalVisible} animationType="slide" transparent>
        <View style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Subir documento PDF</Text>
            <TouchableOpacity
              style={styles.button}
              onPress={handleSelectFile}
            >
              <Text style={styles.buttonText}>Elegir archivo PDF</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[styles.button, { backgroundColor: '#999' }]}
              onPress={() => setModalVisible(false)}
            >
              <Text style={styles.buttonText}>Cancelar</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>

      {/* Modal confirmación */}
      <Modal visible={confirmModalVisible} animationType="slide" transparent>
        <View style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Solicitud enviada correctamente</Text>
            <TouchableOpacity
              style={styles.button}
              onPress={handleConfirm}
            >
              <Text style={styles.buttonText}>Aceptar</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f2f2f2',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 12,
    textAlign: 'center',
  },
  label: {
    marginTop: 12,
    fontSize: 16,
    fontWeight: 'bold',
  },
  pickerContainer: {
    backgroundColor: '#fff',
    marginVertical: 8,
    borderRadius: 8,
    overflow: 'hidden',
  },
  input: {
    backgroundColor: '#fff',
    padding: 12,
    marginVertical: 8,
    borderRadius: 8,
  },
  button: {
    backgroundColor: '#4CAF50',
    padding: 14,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 16,
  },
  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  fileInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 12,
  },
  modalContainer: {
    flex: 1,
    justifyContent: 'center',
    backgroundColor: 'rgba(0,0,0,0.4)',
  },
  modalContent: {
    backgroundColor: '#fff',
    padding: 20,
    margin: 20,
    borderRadius: 10,
    alignItems: 'center',
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 20,
  },
});
