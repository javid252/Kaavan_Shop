<template>
  <div class="route-line" :style="{ margin: margin }">
    <span class="route-line__dot" />
    <span class="route-line__track" />
    <span class="route-line__dot" />
  </div>
</template>

<script>
export default {
  name: "RouteDivider",
  props: {
    margin: { type: String, default: "32px 0" },
  },
};
</script>
