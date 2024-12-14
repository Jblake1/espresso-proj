<!-- components/NewTodo.svelte -->
<script lang='ts'>
  import { onMount } from 'svelte'
  import { selectOnFocus } from '../actions'
  

  const { autofocus } = $props<{ autofocus: boolean }>()

  let name = $state('');
  let machine = $state('');
  let coffeeType = $state('');
  let grinder = $state('');
  let beanType = $state('');
  let advice = $state('');
  let brewTime = $state('');
  let grindSetting = $state('');

  let nameEl: HTMLInputElement;
  let machineEl: HTMLInputElement;
  let coffeeTypeEl: HTMLInputElement;
  let grinderEl: HTMLInputElement;
  let beanTypeEl: HTMLInputElement;
  let adviceEl: HTMLInputElement;
  let brewTimeEl: HTMLInputElement;
  let grindSettingEl: HTMLInputElement;
  
  
    //on:submit|preventDefault={submit} on:keydown={e => e.key === 'Escape' && onCancel()}

  const submit = async () => {
    try {
      const response = await fetch('http://localhost:4000/recommendation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          machine,
          coffee_type: coffeeType,
          grinder,
          coffee_beans: beanType
        })
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log('Received data:', data);
      const advice = data.advice;
      console.log('Advice:', advice);
      brewTime = String(advice.brew_time); // Extract and convert "brew_time" to a string
      console.log('Brew Time:', brewTime);
      grindSetting = advice.grind_setting; // Extract and convert "brew_time" to a string
      console.log('Grind Setting:', grindSetting);

    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    }
  }
  

  const onCancel = () => {
    name = ''
    machine = '';
    coffeeType = '';
    grinder = '';
    beanType = '';
    advice = '';
    brewTime = '';
    grindSetting = '';
    nameEl.focus()            // give focus to the name input
  }

  
  onMount(() => autofocus && nameEl.focus && nameEl.focus())    // if autofocus is true, we run nameEl.focus()

</script>

<style>
  .visible-heading {
  display: block !important;
  visibility: visible !important;
  opacity: 1 !important;
  color: black !important;
  font-size: 1.2em !important;
  margin-top: 1em !important;
}
</style>

<form >
  <h2 class="label-wrapper">
    <label for="machine" class="label__lg">Coffee Machine</label>
  </h2>
  <input bind:value={machine} bind:this={machineEl} use:selectOnFocus 
    type="text" id="machine" autoComplete="off" class="input input__lg" 
  />

  <h2 class="label-wrapper">
    <label for="coffeeType" class="label__lg">Coffee Type</label>
  </h2>
  <input bind:value={coffeeType} bind:this={coffeeTypeEl} use:selectOnFocus 
    type="text" id="coffeeType" autoComplete="off" class="input input__lg" 
  />

  <h2 class="label-wrapper">
    <label for="grinder" class="label__lg">Grinder Type</label>
  </h2>
  <input bind:value={grinder} bind:this={grinderEl} use:selectOnFocus 
    type="text" id="grinder" autoComplete="off" class="input input__lg" 
  />

  <h2 class="label-wrapper">
    <label for="beanType" class="label__lg">Bean Type</label>
  </h2>
  <input bind:value={beanType} bind:this={beanTypeEl} use:selectOnFocus 
    type="text" id="beanType" autoComplete="off" class="input input__lg" 
  />

  <h2 class="label-wrapper">
    <label for="grindSetting" class="label__lg">Grind Setting</label>
  </h2>
  <input bind:value={grindSetting} bind:this={beanTypeEl} use:selectOnFocus 
    type="text" id="grindSetting" autoComplete="off" class="input input__lg" 
  />

  <h1 class="visible-heading">
    Grind Setting:{grindSetting}
  </h1>

  <h1 class="visible-heading">
    Brew Time:{brewTime}
  </h1>

  <button type="submit" disabled={false} class="btn btn__primary btn__lg" onclick={submit} >Submit</button>

</form>
