<script lang="ts">
  export let verboseName: string;
  export let name: string;
  export let required: boolean;
</script>

<input
  id={name}
  {name}
  type="checkbox"
  {required}
  class="h-4 w-4 rounded border-whisper-dark text-willow-grove focus:ring-willow-grove"
/>
<label for={name} class="ml-3 block text-sm leading-6 text-marshland">{verboseName}</label>
