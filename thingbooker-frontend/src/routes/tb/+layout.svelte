<script lang="ts">
  import NavbarButton from '$lib/components/NavbarButton.svelte';
  import { CalendarSvg, GroupSvg, HamburgerMenuSvg, HouseSvg } from '$lib/components/svg';
  import { BASE_LOGGEDIN_URL } from '$lib/utils/constants';

  const getSvgStrokeClass = (active: boolean) => {
    return active ? 'stroke-whisper' : 'stroke-whisper-dark';
  };
</script>

<header class="sticky top-0">
  <nav class="h-20 bg-willow-grove rounded-b-lg">
    <ul class="flex justify-between items-center h-full mx-5">
      <li><HamburgerMenuSvg /></li>
      <li><a href="{BASE_LOGGEDIN_URL}/me">User</a></li>
    </ul>
  </nav>
</header>

<main class="mb-auto flex-grow mx-4">
  <div class="mt-4">
    <slot />
  </div>
</main>

<footer class="sticky bottom-0">
  <nav class="h-24 bg-willow-grove flex items-center rounded-t-lg">
    <ul class="flex justify-around w-full text-whisper-dark">
      <li>
        <NavbarButton linkTo="{BASE_LOGGEDIN_URL}/book" let:active>
          <CalendarSvg classes={getSvgStrokeClass(active)} />
          <span class:text-whisper={active}>Bookings</span>
        </NavbarButton>
      </li>
      <li>
        <NavbarButton linkTo="{BASE_LOGGEDIN_URL}/things" let:active>
          <HouseSvg classes={getSvgStrokeClass(active)} />
          <span class:text-whisper={active}>Ting</span>
        </NavbarButton>
      </li>
      <li>
        <NavbarButton linkTo="{BASE_LOGGEDIN_URL}/groups" let:active>
          <GroupSvg classes={getSvgStrokeClass(active)} />
          <span class:text-whisper={active}>Grupper</span>
        </NavbarButton>
      </li>
    </ul>
  </nav>
</footer>
