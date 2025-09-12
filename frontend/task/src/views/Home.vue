<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Navbar -->
    <nav class="bg-blue-600 text-white px-6 py-4 flex justify-between items-center shadow-md">
      <h1 class="text-xl font-bold">Gestor de Tareas</h1>
      <div class="flex items-center space-x-4">
        <span class="font-medium">👤 {{ user.name }}</span>
        <button @click="logout"
                class="bg-red-500 px-3 py-1 rounded hover:bg-red-600 transition">
          Cerrar sesión
        </button>
      </div>
    </nav>

    <!-- Contenido -->
    <main class="p-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-2xl font-semibold text-gray-800">Mis Tareas</h2>
        <button @click="openModal"
                class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition">
          + Nueva Tarea
        </button>
      </div>

      <!-- Loader -->
      <p v-if="loading" class="text-gray-500">Cargando tareas...</p>

      <!-- Tabla de tareas -->
      <table v-else class="w-full bg-white shadow-md rounded-lg overflow-hidden">
        <thead class="bg-gray-200">
          <tr>
            <th class="px-4 py-2 text-left">Título</th>
            <th class="px-4 py-2 text-left">Descripción</th>
            <th class="px-4 py-2 text-left">Estado</th>
            <th class="px-4 py-2 text-left">Creado</th>
            <th class="px-4 py-2 text-left">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in tasks" :key="task.id" class="border-b hover:bg-gray-50">
            <td class="px-4 py-2 font-medium">{{ task.title }}</td>
            <td class="px-4 py-2">{{ task.description }}</td>
            <td class="px-4 py-2">
              <span 
                :class="{
                  'bg-yellow-200 text-yellow-800 px-2 py-1 rounded': task.status === 'pending',
                  'bg-blue-200 text-blue-800 px-2 py-1 rounded': task.status === 'in_progress',
                  'bg-green-200 text-green-800 px-2 py-1 rounded': task.status === 'completed'
                }">
                {{ formatStatus(task.status) }}
              </span>
            </td>
            <td class="px-4 py-2 text-sm text-gray-600">{{ formatDate(task.created_at) }}</td>
            <td class="px-4 py-2 flex space-x-2">
              <button @click="openEditModal(task)"
                      class="px-2 py-1 bg-yellow-400 text-white rounded hover:bg-yellow-500 transition">Editar</button>
              <button @click="deleteTask(task.id)"
                      class="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </main>

    <!-- Modal Nueva Tarea -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div class="bg-white rounded-lg w-full max-w-md p-6 relative">
        <h3 class="text-xl font-bold mb-4">Crear Nueva Tarea</h3>
        <form @submit.prevent="createTask" class="space-y-4">
          <div>
            <label class="block mb-1 text-gray-700">Título</label>
            <input v-model="newTask.title" type="text" required
                   class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />
          </div>
          <div>
            <label class="block mb-1 text-gray-700">Descripción</label>
            <textarea v-model="newTask.description" rows="3" required
                      class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400"></textarea>
          </div>
          <div>
            <label class="block mb-1 text-gray-700">Estado</label>
            <select v-model="newTask.status" required
                    class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400">
              <option value="pending">Pendiente</option>
              <option value="in_progress">En progreso</option>
              <option value="completed">Completada</option>
            </select>
          </div>
          <div class="flex justify-end space-x-2">
            <button type="button" @click="closeModal"
                    class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400 transition">Cancelar</button>
            <button type="submit"
                    class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition">Crear</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Editar Tarea -->
    <div v-if="editModal" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div class="bg-white rounded-lg w-full max-w-md p-6 relative">
        <h3 class="text-xl font-bold mb-4">Editar Tarea</h3>
        <form @submit.prevent="updateTask" class="space-y-4">
          <div>
            <label class="block mb-1 text-gray-700">Título</label>
            <input v-model="editTask.title" type="text" required
                   class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400" />
          </div>
          <div>
            <label class="block mb-1 text-gray-700">Descripción</label>
            <textarea v-model="editTask.description" rows="3" required
                      class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400"></textarea>
          </div>
          <div>
            <label class="block mb-1 text-gray-700">Estado</label>
            <select v-model="editTask.status" required
                    class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400">
              <option value="pending">Pendiente</option>
              <option value="in_progress">En progreso</option>
              <option value="completed">Completada</option>
            </select>
          </div>
          <div class="flex justify-end space-x-2">
            <button type="button" @click="closeEditModal"
                    class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400 transition">Cancelar</button>
            <button type="submit"
                    class="px-4 py-2 bg-yellow-400 text-white rounded hover:bg-yellow-500 transition">Guardar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const API_BASE = 'https://proyecto-aws-5.onrender.com/task/tasks/'

const router = useRouter()
const user = ref({ name: 'Usuario' })
const tasks = ref([])
const loading = ref(true)

// Nueva Tarea
const showModal = ref(false)
const newTask = reactive({ title: '', description: '', status: 'pending' })

// Editar Tarea
const editModal = ref(false)
const editTask = reactive({ id: null, title: '', description: '', status: 'pending' })

// Funciones modal
const openModal = () => {
  newTask.title = ''
  newTask.description = ''
  newTask.status = 'pending'
  showModal.value = true
}
const closeModal = () => showModal.value = false

const openEditModal = (task) => {
  editTask.id = task.id
  editTask.title = task.title
  editTask.description = task.description
  editTask.status = task.status
  editModal.value = true
}
const closeEditModal = () => editModal.value = false

// Cargar tareas
onMounted(async () => {
  const savedUser = localStorage.getItem('user')
  const token = localStorage.getItem('token')
  if (!savedUser || !token) return router.push('/')
  user.value = JSON.parse(savedUser)
  await loadTasks(token)
})

const loadTasks = async (token) => {
  loading.value = true
  try {
    const response = await axios.get(API_BASE, { headers: { Authorization: `Bearer ${token}` } })
    tasks.value = response.data
  } catch (error) {
    console.error('Error al cargar tareas', error)
    if (error.response?.status === 401) logout()
  } finally {
    loading.value = false
  }
}

// Crear tarea
const createTask = async () => {
  const token = localStorage.getItem('token')
  try {
    const response = await axios.post(API_BASE, newTask, { headers: { Authorization: `Bearer ${token}` }})
    tasks.value.push(response.data)
    closeModal()
  } catch (error) {
    console.error('Error al crear tarea', error)
    if (error.response?.status === 401) logout()
  }
}

// Actualizar tarea
const updateTask = async () => {
  const token = localStorage.getItem('token')
  try {
    const response = await axios.put(`${API_BASE}${editTask.id}/`, {
      title: editTask.title,
      description: editTask.description,
      status: editTask.status
    }, { headers: { Authorization: `Bearer ${token}` }})
    const index = tasks.value.findIndex(t => t.id === editTask.id)
    if (index !== -1) tasks.value[index] = response.data
    closeEditModal()
  } catch (error) {
    console.error('Error al actualizar tarea', error)
    if (error.response?.status === 401) logout()
  }
}

// Eliminar tarea
const deleteTask = async (id) => {
  if (!confirm('¿Deseas eliminar esta tarea?')) return
  const token = localStorage.getItem('token')
  try {
    await axios.delete(`${API_BASE}${id}/`, { headers: { Authorization: `Bearer ${token}` } })
    tasks.value = tasks.value.filter(t => t.id !== id)
  } catch (error) {
    console.error('Error al eliminar tarea', error)
    if (error.response?.status === 401) logout()
  }
}

// Logout
const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/')
}

// Helpers
const formatStatus = (status) => {
  if (status === 'pending') return 'Pendiente'
  if (status === 'in_progress') return 'En progreso'
  if (status === 'completed') return 'Completada'
  return status
}
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', { year: 'numeric', month: 'short', day: 'numeric', hour:'2-digit', minute:'2-digit' })
}
</script>
