<script lang="ts">
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';
    import JourneyCard from './JourneyCard.svelte';
    
    // Add loading state
    let isLoading = true;

    let journeyImage1 = '/images/espresso1.jpg';
    let journeyImage2 = '/images/espresso2.jpg';
    let journeyImage3 = '/images/espresso3.jpg';
    
    let drink1 = '';
    let grinder1 = '';
    let grindSetting1 = '';
    let coffeeBeans1 = '';
    let brewingDevice1 = '';
    let iteration1 = '';
    let journey_id1 = '';
    let journey_id2 = '';
    let journey_id3 = '';

    let drink2 = '';
    let grinder2 = '';
    let grindSetting2 = '';
    let coffeeBeans2 = '';
    let brewingDevice2 = '';
    let iteration2 = '';

    let drink3 = '';
    let grinder3 = '';
    let grindSetting3 = '';
    let coffeeBeans3 = '';
    let brewingDevice3 = '';
    let iteration3 = '';

    let cardPropData1 = {};
    let cardPropData2 = {};
    let cardPropData3 = {};

    let cardProp1 = () => ({
        journeyID: journey_id1
    });

    let cardProp2 = () => ({
        journeyID: journey_id2
    });

    let cardProp3 = () => ({
        journeyID: journey_id3
    });

    // Add state to track which accordion item is open
    let openItem = -1; // -1 means all closed

    // Function to toggle accordion items
    function toggleAccordion(index) {
        openItem = openItem === index ? -1 : index;
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
                journey_id1 = '';
                journey_id2 = '';
                journey_id3 = '';

                drink1 = drink2 = drink3 = '';
                grinder1 = grinder2 = grinder3 = '';
                coffeeBeans1 = coffeeBeans2 = coffeeBeans3 = '';
                brewingDevice1 = brewingDevice2 = brewingDevice3 = '';

                const data = await response.json();
                console.log('Journey deleted:', data);
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
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Archive:', data);
                const journeys = data.journeys;
                console.log('journeys:', journeys);
                
                if (journeys.length > 0) {
                    // Destructure the first setup object
                    drink1 = journeys[0].drink;
                    grinder1 = journeys[0].grinder;
                    grindSetting1 = journeys[0].grindSetting;
                    coffeeBeans1 = journeys[0].coffeeBeans;
                    brewingDevice1 = journeys[0].brewingDevice;
                    iteration1 = journeys[0].iteration;
                    journey_id1 = journeys[0].id;
                    cardPropData1 = cardProp1();
                }

                if (journeys.length > 1) {
                    // Destructure the second setup object
                    drink2 = journeys[1].drink;
                    grinder2 = journeys[1].grinder;
                    grindSetting2 = journeys[1].grindSetting;
                    coffeeBeans2 = journeys[1].coffeeBeans;
                    brewingDevice2 = journeys[1].brewingDevice;
                    iteration2 = journeys[1].iteration;
                    journey_id2 = journeys[1].id;
                    cardPropData2 = cardProp2();
                }

                if (journeys.length > 2) {
                    // Destructure the third setup object
                    drink3 = journeys[2].drink;
                    grinder3 = journeys[2].grinder;
                    grindSetting3 = journeys[2].grindSetting;
                    coffeeBeans3 = journeys[2].coffeeBeans;
                    brewingDevice3 = journeys[2].brewingDevice;
                    iteration3 = journeys[2].iteration;
                    journey_id3 = journeys[2].id;
                    cardPropData3 = cardProp3();
                }
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

<div class="flex flex-row w-full">
    <div class="flex flex-col items-start gap-7 w-3/4">
        {#if isLoading}
            <div class="w-full flex justify-center items-center p-10">
                <div class="border-4 border-transparent border-t-primary-500 rounded-full w-10 h-10 animate-spin"></div>
            </div>
        {:else if journey_id1 || journey_id2 || journey_id3}
            <Accordion class="w-full">
                {#if journey_id1}
                    <!-- First Journey -->
                    <AccordionItem open={openItem === 0}>
                        <svelte:fragment slot="lead">
                            <div class="flex items-center space-x-2">
                                <span class="badge bg-primary-500">1</span>
                            </div>
                        </svelte:fragment>
                        <svelte:fragment slot="summary">
                            <button
                                type="button"
                                class="flex items-center space-x-3 w-full text-left h-10 p-0 overflow-hidden" 
                                style="background-image: url({journeyImage1}); background-size: cover; background-position: center;"
                                on:click|stopPropagation={() => toggleAccordion(0)}
                                on:keydown={(e) => e.key === 'Enter' && toggleAccordion(0)}
                            >
                                <div class="py-0 px-3 rounded-md flex items-center space-x-3 flex-grow">
                                    <p class="whitespace-nowrap bg-primary-500/80 px-2 py-0.5 rounded text-white text-sm">{drink1}</p>
                                    <div class="h-3 border-r border-slate-300"></div>
                                    <p class="whitespace-nowrap truncate bg-primary-500/80 px-2 py-0.5 rounded text-white text-sm">{coffeeBeans1}</p>
                                </div>
                                <div>
                                    <span 
                                        class="btn-icon variant-filled-primary cursor-pointer"
                                        on:click|stopPropagation={() => deleteJourney(journey_id1)}
                                        on:keydown|stopPropagation={(e) => e.key === 'Enter' && deleteJourney(journey_id1)}
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
                                                <p class="whitespace-nowrap">{drink1}</p>
                                                <div class="h-4 border-r border-slate-300"></div>
                                                <p class="whitespace-nowrap">{coffeeBeans1}</p>
                                                <div class="h-4 border-r border-slate-300"></div>
                                                <p class="whitespace-nowrap">{grinder1}</p>
                                                <div class="h-4 border-r border-slate-300"></div>
                                                <p class="whitespace-nowrap">{brewingDevice1}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="flex justify-center w-full">
                                    <div class="w-full md:w-3/4">
                                        <JourneyCard journeyData={cardPropData1}/>
                                    </div>
                                </div>
                            </div>
                        </svelte:fragment>
                    </AccordionItem>
                {/if}
                
                <!-- Second Journey -->
                {#if journey_id2}
                    <AccordionItem open={openItem === 1}>
                        <svelte:fragment slot="lead">
                            <div class="flex items-center space-x-2">
                                <span class="badge bg-primary-500">2</span>
                            </div>
                        </svelte:fragment>
                        <svelte:fragment slot="summary">
                            <button
                                type="button"
                                class="flex items-center space-x-3 w-full text-left h-10 p-0 overflow-hidden" 
                                style="background-image: url({journeyImage2}); background-size: cover; background-position: center;"
                                on:click|stopPropagation={() => toggleAccordion(1)}
                                on:keydown={(e) => e.key === 'Enter' && toggleAccordion(1)}
                            >
                                <div class="py-0 px-3 rounded-md flex items-center space-x-3 flex-grow">
                                    <p class="whitespace-nowrap bg-primary-500/80 px-2 py-0.5 rounded text-white text-sm">{drink2}</p>
                                    <div class="h-3 border-r border-slate-300"></div>
                                    <p class="whitespace-nowrap truncate bg-primary-500/80 px-2 py-0.5 rounded text-white text-sm">{coffeeBeans2}</p>
                                </div>
                                <div>
                                    <span 
                                        class="btn-icon variant-filled-primary cursor-pointer"
                                        on:click|stopPropagation={() => deleteJourney(journey_id2)}
                                        on:keydown|stopPropagation={(e) => e.key === 'Enter' && deleteJourney(journey_id2)}
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
                                                <p class="whitespace-nowrap">{drink2}</p>
                                                <div class="h-4 border-r border-slate-300"></div>
                                                <p class="whitespace-nowrap">{coffeeBeans2}</p>
                                                <div class="h-4 border-r border-slate-300"></div>
                                                <p class="whitespace-nowrap">{grinder2}</p>
                                                <div class="h-4 border-r border-slate-300"></div>
                                                <p class="whitespace-nowrap">{brewingDevice2}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="flex justify-center w-full">
                                    <div class="w-full md:w-3/4">
                                        <JourneyCard journeyData={cardPropData2}/>
                                    </div>
                                </div>
                            </div>
                        </svelte:fragment>
                    </AccordionItem>
                {/if}

                <!-- Third Journey -->
                {#if journey_id3}
                    <AccordionItem open={openItem === 2}>
                        <svelte:fragment slot="lead">
                            <div class="flex items-center space-x-2">
                                <span class="badge bg-primary-500">3</span>
                            </div>
                        </svelte:fragment>
                        <svelte:fragment slot="summary">
                            <button
                                type="button"
                                class="flex items-center space-x-3 w-full text-left h-10 p-0 overflow-hidden" 
                                style="background-image: url({journeyImage3}); background-size: cover; background-position: center;"
                                on:click|stopPropagation={() => toggleAccordion(2)}
                                on:keydown={(e) => e.key === 'Enter' && toggleAccordion(2)}
                            >
                                <div class="py-0 px-3 rounded-md flex items-center space-x-3 flex-grow">
                                    <p class="whitespace-nowrap bg-primary-500/80 px-2 py-0.5 rounded text-white text-sm">{drink3}</p>
                                    <div class="h-3 border-r border-slate-300"></div>
                                    <p class="whitespace-nowrap truncate bg-primary-500/80 px-2 py-0.5 rounded text-white text-sm">{coffeeBeans3}</p>
                                </div>
                                <div>
                                    <span 
                                        class="btn-icon variant-filled-primary cursor-pointer"
                                        on:click|stopPropagation={() => deleteJourney(journey_id3)}
                                        on:keydown|stopPropagation={(e) => e.key === 'Enter' && deleteJourney(journey_id3)}
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
                                                <p class="whitespace-nowrap">{drink3}</p>
                                                <div class="h-4 border-r border-slate-300"></div>
                                                <p class="whitespace-nowrap">{coffeeBeans3}</p>
                                                <div class="h-4 border-r border-slate-300"></div>
                                                <p class="whitespace-nowrap">{grinder3}</p>
                                                <div class="h-4 border-r border-slate-300"></div>
                                                <p class="whitespace-nowrap">{brewingDevice3}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="flex justify-center w-full">
                                    <div class="w-full md:w-3/4">
                                        <JourneyCard journeyData={cardPropData3}/>
                                    </div>
                                </div>
                            </div>
                        </svelte:fragment>
                    </AccordionItem>
                {/if}
            </Accordion>
        {:else}
            <div class="w-full text-center p-10 border border-primary-200 rounded-lg bg-tertiary-900/50">
                <p class="text-xl font-semibold text-tertiary-200">No Archives</p>
                <p class="mt-2 text-tertiary-400">No coffee records have been created yet!?</p>
                <a href="/" class="btn variant-filled-primary mt-6">Get a settings recommendation</a>
            </div>
        {/if}
    </div>
</div>

<style>
    :global(.accordion-item) {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }
    
    :global(.accordion-item + .accordion-item) {
        margin-top: 1px !important;
    }
</style>