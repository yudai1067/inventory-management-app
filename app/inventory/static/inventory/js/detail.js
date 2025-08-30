document.addEventListener("DOMContentLoaded", () => {
    const editProductSwitch = document.getElementById("edit-product-switch");
    const productForm = document.getElementById("product-form");
    let isEditing = false;

    editProductSwitch.addEventListener("click", () => {
        isEditing = !isEditing;
        productForm.querySelectorAll("input, textarea, button[type='submit']").forEach(el => {
            el.disabled = !isEditing;
        });
        editProductSwitch.nextElementSibling.textContent = isEditing ? "編集モード: ON" : "編集モード: OFF";
    });
});
