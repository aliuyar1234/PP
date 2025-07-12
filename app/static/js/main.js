const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const fileList = document.getElementById('file-list');

uploadArea.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
});

function handleFiles(files) {
    for (const file of files) {
        uploadFile(file);
    }
}

function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const fileItem = document.createElement('div');
        fileItem.classList.add('file-item');
        fileItem.innerHTML = `
            <div>
                <p><strong>Original:</strong> ${data.original_filename}</p>
                <p><strong>New:</strong> <input type="text" value="${data.new_filename}" class="new-filename-input"></p>
            </div>
            <button class="approve-btn">Approve</button>
        `;
        fileList.appendChild(fileItem);

        fileItem.querySelector('.approve-btn').addEventListener('click', () => {
            const newName = fileItem.querySelector('.new-filename-input').value;
            // Here you would typically send the new name to the server to finalize the rename
            alert(`Approved new name: ${newName}`);
            fileItem.classList.add('approved');
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
