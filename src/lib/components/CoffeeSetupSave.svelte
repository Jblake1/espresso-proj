<script lang="ts">
    let props   = $props();
   
    const saveSetup = async () => {
      try {
        const response = await fetch('http://localhost:4000/saveSetup', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(
            {
              drink: props.drink.drink,
              brewingDevice: props.drink.brewingDevice,
              grinder: props.drink.grinder,
              grindSetting: props.drink.grindSetting,
              coffeeBeans: props.drink.coffeeBeans
            }
          ),
        });
  
        if (response.ok) {
          alert('Setup saved successfully!');
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
  
  <form>
    <button on:click={saveSetup}>Save Setup</button>
  </form>