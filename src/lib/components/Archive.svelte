<script lang="ts">
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';
    import JourneyCard from './JourneyCard.svelte';
    
    // Add loading state
    let isLoading = true;
    
    // Store all journeys in an array
    let journeys = [];
    
    // An array of background images to cycle through
    const journeyImages = [
        '/images/espresso1.jpg',
        '/images/espresso2.jpg',
        '/images/espresso3.jpg'
    ];

    const espresso_machine = '/images/espresso_machine.png';
    
    // Add state to track which accordion item is open
    let openItem = -1; // -1 means all closed

    // Function to toggle accordion items
    function toggleAccordion(index) {
        openItem = openItem === index ? -1 : index;
    }

    // Get image for a journey based on its index
    function getImageForIndex(index) {
        return journeyImages[index % journeyImages.length];
    }

    // Create card prop data for a journey
    function createCardPropData(journey) {
        return { journeyID: journey.id };
    }

    const deleteJourney = async (journeyID) => {
        try {
            const response = await fetch('http://localhost:4000/journeyDelete', {
                method: 'Post',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id: journeyID
                }),
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Journey deleted:', data);
                // Refresh journeys after deletion
                displayArchive();
            } else {
                const error = await response.json();
                console.error('Failed to delete journey:', error.message);
            }
        } catch (err) {
            console.error('Error deleting journey:', err);
        }
    }

    const displayArchive = async () => {
        isLoading = true;
        try {
            const response = await fetch('http://localhost:4000/archiveSetup', {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Archive:', data);
                journeys = data.journeys || [];
                console.log('journeys:', journeys);
            } else {
                const error = await response.json();
                console.error('Failed to fetch journeys:', error.message);
            }
        } catch (err) {
            console.error('Error fetching journeys:', err);
        } finally {
            isLoading = false;
        }
    }

    onMount(() => {
        displayArchive();
    });
</script>

<style>
    :global(.accordion-item) {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }
    
    :global(.accordion-item + .accordion-item) {
        margin-top: 1px !important;
    }

    /* Add styles for the espresso machine image */
    img {
        max-height: 70vh;
        object-fit: contain;
        transition: transform 0.3s ease;
    }
    
</style>

<div class="flex flex-row w-full">
    <div class="flex flex-col items-start gap-7 w-3/4">
        {#if isLoading}
            <div class="w-full flex justify-center items-center p-10">
                <div class="border-4 border-transparent border-t-primary-500 rounded-full w-10 h-10 animate-spin"></div>
            </div>
        {:else if journeys.length > 0}
            <Accordion class="w-full">
                {#each journeys as journey, index}
                    <AccordionItem open={openItem === index}>
                        <svelte:fragment slot="lead">
                            <div class="flex items-center space-x-2">
                                <span class="badge bg-primary-500">{index + 1}</span>
                            </div>
                        </svelte:fragment>
                        <svelte:fragment slot="summary">
                            <button
                                type="button"
                                class="flex items-center space-x-3 w-full text-left h-10 p-0 overflow-hidden" 
                                style="background-image: url({getImageForIndex(index)}); background-size: cover; background-position: center;"
                                on:click|stopPropagation={() => toggleAccordion(index)}
                                on:keydown={(e) => e.key === 'Enter' && toggleAccordion(index)}
                            >
                                <div class="py-0 px-3 rounded-md flex items-center space-x-3 flex-grow">
                                    <p class="whitespace-nowrap bg-primary-500/80 px-2 py-0.5 rounded text-white text-sm">{journey.drink}</p>
                                    <div class="h-3 border-r border-slate-300"></div>
                                    <p class="whitespace-nowrap truncate bg-primary-500/80 px-2 py-0.5 rounded text-white text-sm">{journey.coffeeBeans}</p>
                                </div>
                                <div>
                                    <span 
                                        class="btn-icon variant-filled-primary cursor-pointer"
                                        on:click|stopPropagation={() => deleteJourney(journey.id)}
                                        on:keydown|stopPropagation={(e) => e.key === 'Enter' && deleteJourney(journey.id)}
                                        tabindex="0"
                                        role="button"
                                        aria-label="Delete journey"
                                    >
                                        delete
                                    </span>
                                </div>
                                <div class="h-full w-12 max-w-[48px] flex-shrink-0"></div>
                            </button>
                        </svelte:fragment>
                        <svelte:fragment slot="content">
                            <div class="journey-content">
                                <div class="w-full rounded-md overflow-hidden">
                                    <div class="p-4">
                                        <div class="flex items-center justify-center">
                                            <div class="flex items-center space-x-3 flex-wrap">
                                                <p class="whitespace-nowrap">{journey.drink}</p>
                                                <div class="h-4 border-r border-slate-300"></div>
                                                <p class="whitespace-nowrap">{journey.coffeeBeans}</p>
                                                <div class="h-4 border-r border-slate-300"></div>
                                                <p class="whitespace-nowrap">{journey.grinder}</p>
                                                <div class="h-4 border-r border-slate-300"></div>
                                                <p class="whitespace-nowrap">{journey.brewingDevice}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="flex justify-center w-full">
                                    <div class="w-full md:w-3/4">
                                        <JourneyCard journeyData={createCardPropData(journey)}/>
                                    </div>
                                </div>
                            </div>
                        </svelte:fragment>
                    </AccordionItem>
                {/each}
            </Accordion>
        {:else}
            <div class="w-full text-center p-10 border border-primary-200 rounded-lg bg-tertiary-900/50">
                <p class="text-xl font-semibold text-tertiary-200">No Archives</p>
                <p class="mt-2 text-tertiary-400">No coffee records have been created yet!?</p>
                <a href="/" class="btn variant-filled-primary mt-6">Get a settings recommendation</a>
            </div>
        {/if}
    </div>

    <!-- Right side: Fixed espresso machine image -->
    <div class="hidden md:block w-1/4 relative">
        <div class="p-4">
            <img src={espresso_machine} alt="Espresso Machine" class="w-full max-w-xs mx-auto drop-shadow-xl" />
        </div>
    </div>
</div>

