<script lang="ts">
  import type { Color } from '$lib/types';
  import { textColorMap, hoverTextColorMap } from '$lib/utils/style';

  export let href: string;
  export let linkText: string;
  export let linkColor: Color = 'tropaz';
</script>

<a {href} class="font-semibold {textColorMap[linkColor]} {hoverTextColorMap[linkColor]}">
  {linkText}
</a>
