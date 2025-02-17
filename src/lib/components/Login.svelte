<!-- Login page which redirects to home upon login 
 returns error msgs for failed login
 redirect to register page for non existing users -->

<script lang="ts">
    import { onMount } from 'svelte'
    import { selectOnFocus } from '../actions'
  
    let email = $state('');
    let password = $state('');
    let emailEl: HTMLInputElement;
    let passwordEl: HTMLInputElement;
    let errorMessage = $state('');
  
    const login = async () => {
      try {
          const response = await fetch('http://localhost:4000/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              email,
              password
            })
          });
    
          if (response.ok) {
            const data = await response.json();
            if (data.message === 'login successful') {
              console.log('Login successful:', data);
              // Redirect to the home page
              window.location.href = '/';
            } else {
              throw new Error('Login failed');
            }
          }
          
          
          // if (!response.ok) {
          //   const errorText = await response.text();
          //   throw new Error(`Login failed: ${errorText}`);
          // }
    
          const data = await response.json();
          console.log('Login successful:', data);
        
      } catch (error) {
        console.error('There was a problem with the login operation:', error);
        errorMessage = 'Login Unsuccessful. Please check email and password';
      }
    };
  
    const onCancel = () => {
      email = '';
      password = '';
      emailEl.focus();
    };
  
    onMount(() => {
      emailEl.focus();
    });
    
</script>

  
<style>
    .error-message {
        color: red;
        margin-top: 1em;
    }
</style>
  
<form on:submit|preventDefault={login}>
  <h2>Login</h2>

  {#if errorMessage}
      <p class="error">{errorMessage}</p>
  {/if}

  <label for="email">Email</label>
  <input type="email" id="email" bind:value={email} required />

  <label for="password">Password</label>
  <input type="password" id="password" bind:value={password} required />

  <button type="submit" class="btn btn__primary btn__lg">Login</button>
  <button type="button" on:click={onCancel} class="btn btn__secondary btn__lg">Cancel</button>
</form>