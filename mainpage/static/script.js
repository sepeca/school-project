document.getElementById('class-select').addEventListener('change', function () {
  let selectedClassId = this.value;
  window.location.href = `/get-schedule/${selectedClassId}`;
});