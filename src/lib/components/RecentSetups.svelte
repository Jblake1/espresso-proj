<!-- displays recently saved espresso setups on homapage
 allow for espresso setups to be archived
 meaning sent to the archive db -->
<script lang="ts">
    import { onMount } from 'svelte';
    import ArchiveButton from './ArchiveButton.svelte';

    let Image1 = '/images/espresso1.jpg';
    let Image2 = '/images/espresso2.jpg';
    let Image3 = '/images/espresso3.jpg';

    let {props, trigger} = $props();

    let drink1 = $state('');
    let grinder1 = $state('');
    let grindSetting1 = $state('');
    let coffeeBeans1 = $state('');
    let brewingDevice1 = $state('');

    let drink2 = $state('');
    let grinder2 = $state('');
    let grindSetting2 = $state('');
    let coffeeBeans2 = $state('');
    let brewingDevice2 = $state('');

    let drink3 = $state('');
    let grinder3 = $state('');
    let grindSetting3 = $state('');
    let coffeeBeans3 = $state('');
    let brewingDevice3 = $state('');

    let drink4 = $state('');
    let grinder4 = $state('');
    let grindSetting4 = $state('');
    let coffeeBeans4 = $state('');
    let brewingDevice4 = $state('');

    let archiveProp1 = () => ({
      drink: drink1,
      grinder: grinder1,
      grindSetting: grindSetting1,
      coffeeBeans: coffeeBeans1,
      brewingDevice: brewingDevice1
    });

    let archiveProp2 = () => ({
      drink: drink2,
      grinder: grinder2,
      grindSetting: grindSetting2,
      coffeeBeans: coffeeBeans2,
      brewingDevice: brewingDevice2
    });

    let archiveProp3 = () => ({
      drink: drink3,
      grinder: grinder3,
      grindSetting: grindSetting3,
      coffeeBeans: coffeeBeans3,
      brewingDevice: brewingDevice3
    });

    let archiveProp4 = () => ({
      drink: drink4,
      grinder: grinder4,
      grindSetting: grindSetting4,
      coffeeBeans: coffeeBeans4,
      brewingDevice: brewingDevice4
    });

    let archivePropData1 = $state({});
    let archivePropData2 = $state({});
    let archivePropData3 = $state({});
    let archivePropData4 = $state({});


    const displaySetups = async () => {
        try {
            const response = await fetch('http://localhost:4000/getSetup', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Recent setups:', data);
                const setups = data.setups;
                console.log('Setups:', setups);
            
            if (setups.length > 0) {
                // Destructure the first setup object
                drink1 = setups[0].drink;
                grinder1 = setups[0].grinder;
                grindSetting1 = setups[0].grindSetting;
                coffeeBeans1 = setups[0].coffeeBeans;
                brewingDevice1 = setups[0].brewingDevice;
                archivePropData1 = archiveProp1();
            }

            if (setups.length > 1) {
                // Destructure the second setup object
                drink2 = setups[1].drink;
                grinder2 = setups[1].grinder;
                grindSetting2 = setups[1].grindSetting;
                coffeeBeans2 = setups[1].coffeeBeans;
                brewingDevice2 = setups[1].brewingDevice;
                archivePropData2 = archiveProp2();
            }

            if (setups.length > 2) {
                // Destructure the third setup object
                drink3 = setups[2].drink;
                grinder3 = setups[2].grinder;
                grindSetting3 = setups[2].grindSetting;
                coffeeBeans3 = setups[2].coffeeBeans;
                brewingDevice3 = setups[2].brewingDevice;
                archivePropData3 = archiveProp3();
            }

            if (setups.length > 3) {
                // Destructure the fourth setup object
                drink4 = setups[3].drink;
                grinder4 = setups[3].grinder;
                grindSetting4 = setups[3].grindSetting;
                coffeeBeans4 = setups[3].coffeeBeans;
                brewingDevice4 = setups[3].brewingDevice;
                archivePropData4 = archiveProp4();
            }
            } else {
                const error = await response.json();
                console.error('Failed to fetch recent setups:', error.message);
            }
           

        } catch (err) {
            console.error('Error fetching recent setups:', err);
        }
    }

    onMount(() => {
    displaySetups();
    });

    $effect(() => {
    if (trigger) {
      displaySetups();
    }
    });
</script>

<style>
    .container1 {
      display: flex;
      flex-direction: column;
      width: 200%;
      align-items: flex-start; /* Aligns items to the right */
      padding: 10px;
    }

    .container2 {
      display: flex;
      flex-direction: row;
      width: 200%;
      align-items: flex-start; /* Aligns items to the right */
      padding: 10px;
    }

    .vertical-divider {
      width: 1px;
      height: auto;
      align-self: stretch;
      background-color: #ccc;
      margin: 0 15px;
    }
  
    .setup {
      text-align: left; /* Aligns text to the right */
      margin-bottom: 10px;
    }
</style>

<div class="container1">
  <div class="container2">
    {#if drink1 !== ''}
      <div class="setup">
        <div class="card">
          <header class="card-header py-5 px-3 bg-cover bg-center" style="background-image: url('{Image1}');">
            <span class="font-medium text-white drop-shadow-md bg-primary-500/80 rounded">{coffeeBeans1} | {drink1}</span>
          </header>
          <section class="py-1 px-3">Brewing Device: {brewingDevice1}</section>
          <section class="py-1 px-3">Grinder: {grinder1}</section>
          <div class="flex flex-row items-center justify-between py-2 px-3 cardfooter">
            <footer class="card-footer py-2">Grind Setting: {grindSetting1}</footer>
            <div class="ArchiveButton">
              <ArchiveButton drink={archivePropData1} />
            </div>
          </div>
        </div>
      </div>
    {/if}

    <div class="vertical-divider"></div>

    {#if drink2 !== ''}
    <div class="setup">
      <div class="card">
        <header class="card-header py-5 px-3 bg-cover bg-center" style="background-image: url('{Image1}');">
          <span class="font-medium text-white drop-shadow-md bg-primary-500/80 rounded">{coffeeBeans2} | {drink2}</span>
        </header>
        <section class="py-1 px-3">Brewing Device: {brewingDevice2}</section>
        <section class="py-1 px-3">Grinder: {grinder2}</section>
        <div class="flex flex-row items-center justify-between py-2 px-3 cardfooter">
          <footer class="card-footer py-2">Grind Setting: {grindSetting2}</footer>
          <div class="ArchiveButton">
            <ArchiveButton drink={archivePropData2} />
          </div>
        </div>
      </div>
    </div>
    {/if}
  </div>

  <div class="w-full h-px bg-gray-300 my-4 mx-auto max-w-3xl"></div>
  
  <div class="container2">
    {#if drink3 !== ''}
      <div class="setup">
        <div class="card">
          <header class="card-header py-5 px-3 bg-cover bg-center" style="background-image: url('{Image1}');">
            <span class="font-medium text-white drop-shadow-md bg-primary-500/80 rounded">{coffeeBeans3} | {drink3}</span>
          </header>
          <section class="py-1 px-3">Brewing Device: {brewingDevice3}</section>
          <section class="py-1 px-3">Grinder: {grinder3}</section>
          <div class="flex flex-row items-center justify-between py-2 px-3 cardfooter">
            <footer class="card-footer py-2">Grind Setting: {grindSetting3}</footer>
            <div class="ArchiveButton">
              <ArchiveButton drink={archivePropData3} />
            </div>
          </div>
        </div>
      </div>
    {/if}

    <div class="vertical-divider"></div>

    {#if drink4 !== ''}
      <div class="setup">
        <div class="card">
          <header class="card-header py-5 px-3 bg-cover bg-center" style="background-image: url('{Image1}');">
            <span class="font-medium text-white drop-shadow-md bg-primary-500/80 rounded">{coffeeBeans4} | {drink4}</span>
          </header>
          <section class="py-1 px-3">Brewing Device: {brewingDevice4}</section>
          <section class="py-1 px-3">Grinder: {grinder4}</section>
          <div class="flex flex-row items-center justify-between py-2 px-3 cardfooter">
            <footer class="card-footer py-2">Grind Setting: {grindSetting4}</footer>
            <div class="ArchiveButton">
              <ArchiveButton drink={archivePropData4} />
            </div>
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>