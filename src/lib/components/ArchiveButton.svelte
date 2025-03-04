<!-- Possibly needs renaming 
 child compponent of recent setups 
 sends selected recent setup to the archive db -->

<script lang="ts">
    let props   = $props();

    const archiveSetup = async () => {
        try {
            const response = await fetch('http://localhost:4000/archiveSetup', {
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
                alert('Setup archived successfully!');
            } else {
                const error = await response.json();
                alert('Failed to archive setup: ' + error.message);
            }
        } catch (err) {
            console.error('Error archiving setup:', err);
            alert('An error occurred while archiving the setup.');
        }
    }
</script>

<div>
    <button type="button" class="btn btn-sm variant-filled" onclick={() => archiveSetup()}>Archive</button>
</div>