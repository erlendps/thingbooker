<script lang="ts">
  import type { Color } from '$lib/types';
  import {
    fillColorMap,
    hoverFillColorMap,
    textColorMap,
    focusOutlineColorMap
  } from '$lib/utils/style';

  export let buttonText: string;
  export let type: 'submit' | 'button' = 'button';
  export let onClick: (e: MouseEvent) => void = (_) => {};
  export let textColor: Color = 'whisper';
  export let fillColor: Color = 'willow-grove';
  export let classes: string = '';
</script>

<button
  {type}
  on:click={onClick}
  class="rounded-full {fillColorMap[fillColor]} px-3 py-1.5 text-sm font-semibold {textColorMap[
    textColor
  ]} shadow-sm {hoverFillColorMap[
    fillColor
  ]} focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 {focusOutlineColorMap[
    fillColor
  ]} {classes}"
>
  {buttonText}
</button>
