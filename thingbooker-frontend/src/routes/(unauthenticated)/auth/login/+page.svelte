<script lang="ts">
  import { enhance } from '$app/forms';
  import Input from '$lib/components/forms/Input.svelte';
  import Checkbox from '$lib/components/forms/Checkbox.svelte';
  import Button from '$lib/components/Button.svelte';
  import Link from '$lib/components/Link.svelte';
  import brandShort from '$lib/assets/brand/brand_square_adv.svg';

  export let form;
</script>

<div class="flex min-h-full flex-col justify-center py-12 sm:px-6 lg:px-8">
  <div class="sm:mx-auto sm:w-full sm:max-w-md">
    <img class="mx-auto h-24 w-auto" src={brandShort} alt="Thingbooker logo" />
    <h2 class="mt-6 text-center text-2xl font-bold leading-9 tracking-tight text-marshland">
      Hei!<br />Vennligst logg inn for å bruke Thingbooker
    </h2>
  </div>
  <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-[480px]">
    <div class="bg-whisper px-6 pt-5 pb-12 shadow sm:rounded-lg sm:px-12">
      <div class="h-5 mb-2">
        {#if form?.error}
          <p class="text-solid-pink text-sm">{form.error}</p>
        {/if}
      </div>
      <form class="space-y-6" action="?/login" method="POST" use:enhance>
        <div>
          <Input
            autocomplete="email"
            verboseName="E-postadresse"
            name="email"
            required={true}
            type="email"
            value={form?.email ?? ''}
          />
        </div>
        <div>
          <Input
            autocomplete="current-password"
            verboseName="Passord"
            name="password"
            required={true}
            type="password"
          />
        </div>

        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <Checkbox name="remember-me" verboseName="Husk på meg" required={false} />
          </div>

          <div class="text-sm leading-6">
            <Link href="#" linkText="Har du glemt passordet?" />
          </div>
        </div>

        <div>
          <Button type="submit" buttonText="Logg inn" classes="py-2 flex w-full justify-center" />
        </div>
      </form>
      <p class="mt-10 text-center text-sm text-gray-500">
        Har du ingen bruker?
        <span class="leading-6">
          <Link href="#" linkText="Lag en bruker her!" />
        </span>
      </p>
    </div>
  </div>
</div>
