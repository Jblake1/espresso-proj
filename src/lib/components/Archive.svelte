<script lang="ts">
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';
    import JourneyCard from './JourneyCard.svelte';
    
    // Add loading state
    let isLoading = true;

    let drink = $state('');
    let isSubmitting = $state(false);

    let isMobile = false;


    if (typeof window !== 'undefined') {
        isMobile = window.innerWidth < 768; // Adjust the breakpoint as needed
        window.addEventListener('resize', () => {
            isMobile = window.innerWidth < 768;
        });
    }
    // Store all journeys in an array
    let journeys = $state([]);
   
    let filteredJourneys = $derived(
        drink ? journeys.filter(journey => journey.drink === drink) : journeys
    );
    
    // An array of background images to cycle through
    const journeyImages = [
        '/images/espresso1.jpg',
        '/images/espresso2.jpg',
        '/images/espresso3.jpg'
    ];

    const espresso_machine = '/images/espresso_machine.png';
    
    // Add state to track which accordion item is open
    let openItem = $state(-1); // -1 means all closed

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

    function truncateText(text: string, maxLength: number): string {
        if (!text) return '';
        return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    }

    function getTruncatedCoffeeBeans(coffeeBeans: string): string {
        return isMobile ? truncateText(coffeeBeans, 16) : truncateText(coffeeBeans, 40);
    }

    const deleteJourney = async (journeyID) => {
        try {
            const response = await fetch('/journeyDelete', {
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
            const response = await fetch('/archiveSetup', {
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

    const submit = (event: Event) => { // Added type for event
        event.preventDefault();
    };

    onMount(async () => {
        await displayArchive();
    });
</script>

<style>
    /* Keep existing styles */
    :global(.accordion-item) {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }

    :global(.accordion-item + .accordion-item) {
        margin-top: 1px !important;
    }


    img {
        max-height: 70vh;
        object-fit: contain;
        transition: transform 0.3s ease;
    }
</style>

<div class="flex-col w-full">
    <div class="flex justify-center items-center w-full p-0">
        <form onsubmit={submit} class="toDoForm">
            <select bind:value={drink} id="drink" class="select w-full px-3 py-2 border rounded min-h-10 min-w-30">
                <option value="">Select a drink</option>
                <option value="Espresso">Espresso</option>
                <option value="Coffee">Coffee</option>
            </select>
        </form>
    </div>
    <div class="flex flex-row w-full justify-start overflow-hidden">
        <div class="flex flex-col items-start w-full overflow-hidden mx-auto md:w-3/4 md:mx-0">
            {#if isLoading}
                <div class="w-full flex justify-center items-center p-10">
                    <div class="border-4 border-transparent border-t-primary-500 rounded-full w-10 h-10 animate-spin"></div>
                </div>
            {:else if filteredJourneys.length > 0}
                <Accordion class="w-full overflow-hidden">
                    {#each filteredJourneys as journey, index}
                        <AccordionItem open={openItem === index} class="mb-0">
                            <svelte:fragment slot="summary">
                                <div class="py-0 px-3 rounded-md flex items-center justify-between w-full h-10"
                                    style="background-image: url({getImageForIndex(index)}); background-size: cover; background-position: center;"
                                >
                                    <div class="flex items-center space-x-3 overflow-hidden max-w-[calc(100%-4rem)]"> 
                                        <p class="whitespace-nowrap bg-primary-500/80 px-2 py-0.5 rounded text-white text-sm flex-shrink-0">
                                            {journey.drink}
                                        </p>
                                        <div class="h-3 border-r border-slate-300 flex-shrink-0"></div>
                                        <p class="overflow-hidden text-ellipsis whitespace-nowrap bg-primary-500/80 px-2 py-0.5 rounded text-white text-sm flex-1 min-w-0">
                                            {getTruncatedCoffeeBeans(journey.coffeeBeans)}
                                        </p>
                                    </div>
                                </div>
                            </svelte:fragment>

                            <div class="flex-shrink-0"> 
                                <span
                                    class="btn-icon variant-filled-primary cursor-pointer"
                                    onclick={(event) => {
                                        event.stopPropagation();
                                        deleteJourney(journey.id);
                                    }}
                                    onkeydown={(event) => {
                                        if (event.key === 'Enter') {
                                            event.stopPropagation();
                                            deleteJourney(journey.id);
                                        }
                                    }}
                                    tabindex="0"
                                    role="button"
                                    aria-label="Delete journey"
                                >
                                    delete
                                </span>
                            </div>

                            <svelte:fragment slot="content">
                                <div class="w-full">
                                    <!-- removed "overflow-hidden" -->
                                    <div class="w-full rounded-md"> 
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
                                    <div class="flex justify-center w-full">
                                        <div class="w-full md:w-3/4">
                                            <JourneyCard journeyData={createCardPropData(journey)}  drink={journey.drink}/>
                                        </div>
                                    </div>
                                </div>
                            </svelte:fragment>
                        </AccordionItem>
                    {/each}
                </Accordion>
            {:else}
                <div class="w-full text-center p-10 border border-primary-200 rounded-lg bg-tertiary-900/50">
                    <p class="text-xl font-semibold text-tertiary-200">No Notes</p>
                    <p class="mt-2 text-tertiary-400">No coffee records have been created yet!?</p>
                    <a href="/" class="btn variant-filled-primary mt-6">Get a setting recommendation</a>
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
</div>

