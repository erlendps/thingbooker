<script lang="ts">
  import type { IsAuthenticatedType, ShortUserType } from '$lib/types';
  import { BASE_LOGGEDIN_URL } from '$lib/utils/constants';
  import brandLong from '$lib/assets/brand/brand_long_tr.svg';
  import brandShort from '$lib/assets/brand/brand_short_tr.svg';
  import defaultAvatar from '$lib/assets/default_avatar.png';
  import UserAvatar from '$lib/components/UserAvatar.svelte';

  export let data: IsAuthenticatedType;
  $: isAuthenticated = data.isAuthenticated;

  const user: ShortUserType = {
    id: '1234',
    avatar: defaultAvatar,
    first_name: 'Robot',
    username: 'roboman'
  };
</script>

<header>
  <nav class="h-20 bg-willow-grove rounded-b-lg">
    <ul class="flex justify-between items-center h-full mx-5">
      <div class="flex items-center">
        <a href="/">
          <img src={brandLong} alt="Thingbooker logo" class="h-12 sm:block hidden" />
          <img src={brandShort} alt="Thingbooker logo" class="h-12 sm:hidden" />
        </a>
      </div>
      <li>
        {#if isAuthenticated}
          <a href="{BASE_LOGGEDIN_URL}/me">
            <UserAvatar {user} />
          </a>
        {:else}
          <a href="/auth/login" class="text-whisper hover:text-whisper-dark">Logg inn</a>
        {/if}
      </li>
    </ul>
  </nav>
</header>

<main class="mb-auto flex-grow mx-4">
  <div class="mt-4">
    <slot />
  </div>
</main>

<footer class="mt-4 bg-willow-grove h-20 rounded-t-lg flex flex-col items-center">Footer</footer>
