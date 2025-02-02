<script lang="ts">

    let drink = $state('');
    let grinder = $state('');
    let grindSetting = $state('');
    let coffeeBeans = $state('');
    let brewingDevice = $state('');    

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
                drink = setups.drink;
            } else {
                const error = await response.json();
                console.error('Failed to fetch recent setups:', error.message);
            }
           

        } catch (err) {
            console.error('Error fetching recent setups:', err);
        }
    }

</script>

<form>
    <button on:click={displaySetups}>Display Setup</button>
    <h2>Recent Setups: {drink} </h2>
</form>