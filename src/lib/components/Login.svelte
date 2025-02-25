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
  
    // const login = async () => {
    //   try {
    //       const response = await fetch('http://localhost:4000/login', {
    //         method: 'POST',
    //         headers: {
    //           'Content-Type': 'application/json'
    //         },
    //         body: JSON.stringify({
    //           email,
    //           password
    //         })
    //       });
    
    //       if (response.ok) {
    //         const data = await response.json();
    //         if (data.message === 'login successful') {
    //           console.log('Login successful:', data);
    //           // Redirect to the home page
    //           window.location.href = '/';
    //         } else {
    //           throw new Error('Login failed');
    //         }
    //       };

    const handleSubmit = async (event: SubmitEvent) => {
      event.preventDefault();
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
              window.location.href = '/';
            } else {
              throw new Error('Login failed');
            }
          }
    
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
  
<div class="card p-4">
  <form onsubmit={handleSubmit} class="space-y-4">
      <h2 class="h2">Login</h2>

      {#if errorMessage}
          <div class="alert variant-filled-error">{errorMessage}</div>
      {/if}
      <label class="label">
          <span>Email</span>
          <input 
              class="input" 
              type="email" 
              bind:value={email}
              bind:this={emailEl}
              placeholder="Enter your email"
              required
          />
      </label>

      <label class="label">
          <span>Password</span>
          <input 
              class="input" 
              type="password" 
              bind:value={password}
              bind:this={passwordEl}
              placeholder="Enter your password"
              required
          />
      </label>

      <button type="submit" class="btn variant-filled-primary w-full">Login</button>
  </form>
</div>

