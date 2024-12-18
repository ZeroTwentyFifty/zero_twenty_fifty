import { reactive } from 'vue'
import type { FormError, FormSubmitEvent } from '#ui/types'

export function useAuth() {
  const state = reactive({
    email: undefined,
    password: undefined
  })

  const config = useRuntimeConfig()

  const validate = (state: any): FormError[] => {
    const errors = []
    if (!state.email) errors.push({ path: 'email', message: 'Required' })
    if (!state.password) errors.push({ path: 'password', message: 'Required' })
    return errors
  }

  async function onSubmit(event: FormSubmitEvent<any>) {
    try {
      const formData = new URLSearchParams();
      formData.append('grant_type', 'client_credentials');
      formData.append('client_id', event.data.email);
      formData.append('client_secret', event.data.password);

      const response = await fetch(`${config.public.apiBase}/auth/token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to authenticate');
      } 

      const data = await response.json();
      console.log('Authentication successful:', data);
      
      // Store the Bearer token
      const bearerToken = data.access_token;
      localStorage.setItem('bearerToken', bearerToken);
      
      console.log('Bearer token stored for future API calls');
      
      return true; // Indicate successful authentication
    } catch (error) {
      console.error('Authentication error:', error);
      return false; // Indicate failed authentication
    }
  }

  return {
    state,
    validate,
    onSubmit
  }
}
