<script lang="ts">
  export let verboseName: string;
  export let autocomplete: string = 'off';
  export let name: string;
  export let type: 'text' | 'email' | 'password' | 'number';
  export let required: boolean;
  export let minLength = 0;
  export let value: FormDataEntryValue = '';
</script>

<label for={name} class="block text-sm font-medium leading-6 text-marshland">{verboseName}</label>
<div class="mt-2">
  <input
    minlength={minLength}
    id={name}
    {name}
    {type}
    {autocomplete}
    {required}
    {value}
    class="text-marshland block w-full rounded-md border-0 py-1.5 shadow-sm ring-1 ring-inset ring-whisper-dark placeholder:text-whisper-dark focus:ring-2 focus:ring-inset focus:ring-willow-grove sm:text-sm sm:leading-6"
  />
</div>
