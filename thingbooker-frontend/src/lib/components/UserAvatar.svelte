<script lang="ts">
  import type { ShortUserType } from '$lib/types';

  export let user: ShortUserType;
  export let tailwindHeight = 'h-12';
</script>

{#key user}
  <img
    src={user.avatar}
    alt="Avatar til {user.first_name}"
    class="border-whisper border-2 rounded-full bg-marshland {tailwindHeight}"
  />
{/key}
