<!-- saves the current values in the submission fields
 and the grind seting rec that was returned -->
<script lang="ts">
    let { value = $bindable(), props }  = $props();
   
    const saveSetup = async () => {
      try {
        const response = await fetch('/saveSetup', {
          method: 'POST',
          credentials: 'include',
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
          //Toggle value to send rerender trigger
          value = value === '1' ? '0' : '1';

        } else {
          const error = await response.json();
          alert('Failed to save setup: ' + error.message);
        }
      } catch (err) {
        console.error('Error saving setup:', err);
        alert('An error occurred while saving the setup.');
      }
    }

    $effect(() => {
      // Only trigger save if we have all required props
      if (props && props.drink && props.brewingDevice && 
          props.grinder && props.grindSetting && props.coffeeBeans) {
        saveSetup();
      }
    });
    
  </script>
  
  <!-- <div>
    <button onclick={() => saveSetup()}>Save Setup</button>
  </div> -->