<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="bg-white p-10 rounded-2xl shadow-xl w-full max-w-sm transform transition duration-500 hover:scale-105">
      <h2 class="text-3xl font-bold mb-6 text-center text-gray-800">Iniciar Sesión</h2>

      <form @submit.prevent="handleLogin" class="space-y-5">
        <div>
          <label class="block text-gray-700 mb-1">Correo</label>
          <input v-model="email" type="email" required placeholder="ejemplo@correo.com"
                 class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 transition" />
          <p v-if="emailError" class="text-red-500 text-sm mt-1">{{ emailError }}</p>
        </div>

        <div>
          <label class="block text-gray-700 mb-1">Contraseña</label>
          <input v-model="password" type="password" required placeholder="********"
                 class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 transition" />
          <p v-if="passwordError" class="text-red-500 text-sm mt-1">{{ passwordError }}</p>
        </div>

        <button type="submit"
                class="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition font-semibold">
          Iniciar Sesión
        </button>
      </form>

      <div v-if="message" :class="{'text-green-500': success, 'text-red-500': !success}"
           class="mt-4 text-center font-medium transition">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const email = ref('')
const password = ref('')
const message = ref('')
const success = ref(false)

const emailError = ref('')
const passwordError = ref('')

const router = useRouter()

// Validaciones en tiempo real
watch(email, (value) => {
  emailError.value = value.includes('@') ? '' : 'Correo inválido'
})
watch(password, (value) => {
  passwordError.value = value.length >= 6? '' : 'La contraseña debe tener al menos 8 caracteres'
})

const handleLogin = async () => {
  message.value = ''
  if (emailError.value || passwordError.value) {
    message.value = 'Corrige los errores antes de continuar'
    success.value = false
    return
  }

  try {
    const response = await axios.post('http://localhost:8000/api/login/', {
      email: email.value,
      password: password.value
    })

    success.value = true
    message.value = '¡Inicio de sesión exitoso!'

    localStorage.setItem('token', response.data.access)
    localStorage.setItem('user', JSON.stringify(response.data.user))

    // Redirigir a página de inicio después de 1.5s
    setTimeout(() => {
      router.push('/home')
    }, 1500)

  } catch (error) {
    success.value = false
    if (error.response && error.response.data) {
      message.value = error.response.data.detail || 'Credenciales incorrectas'
    } else {
      message.value = 'Error al conectar con el servidor'
    }
  }
}
</script>
