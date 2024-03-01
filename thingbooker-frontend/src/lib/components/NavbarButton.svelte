<script lang="ts">
  import { page } from '$app/stores';

  export let linkTo: string;

  $: active = $page.url.pathname === linkTo;
</script>

<a href={linkTo} class="hover:cursor-pointer">
  {#key active}
    <div
      class="flex flex-col items-center gap-1 border-2 border-transparent"
      class:activeButton={active}
      class:border-b-whisper={active}
    >
      <slot {active} />
    </div>
  {/key}
</a>
