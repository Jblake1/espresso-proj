<script lang="ts">
    let { value = $bindable(), props }  = $props();
   
    const saveSetup = async () => {
      try {
        const response = await fetch('http://localhost:4000/saveSetup', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(
            {
              drink: props.drink,
              brewingDevice: props.brewingDevice,
              grinder: props.grinder,
              grindSetting: props.grindSetting,
              coffeeBeans: props.coffeeBeans
            }
          ),
        });
  
        if (response.ok) {
          alert('Setup saved successfully!');
          value= 'trigger';

        } else {
          const error = await response.json();
          alert('Failed to save setup: ' + error.message);
        }
      } catch (err) {
        console.error('Error saving setup:', err);
        alert('An error occurred while saving the setup.');
      }
    }
  </script>
  
  <div>
    <button onclick={() => saveSetup()}>Save Setup</button>
  </div>