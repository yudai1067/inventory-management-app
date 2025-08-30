document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.delete-form').forEach(form => {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            const btn = form.querySelector('button[type="submit"]');
            const productSku = btn.dataset.productSku;
            if (confirm(`「${productSku}」を削除しますか？`)) {
                form.submit();
            }
        });
    });
});
