function updateSize() {
    let nBytes = 0,
        oFiles = this.files,
        nFiles = oFiles.length;
    let fileNames = [];

    for (let nFileId = 0; nFileId < nFiles; nFileId++) {
        nBytes += oFiles[nFileId].size;
    }

    let tempCount = 0;
    for (let key in oFiles) {
        if (tempCount == nFiles) {
            break
        }
        fileNames.push(oFiles[key]['name']);
        tempCount += 1;
    }
    let sOutput = nBytes + " bytes";
    // optional code for multiples approximation
    const aMultiples = [
        "KiB",
        "MiB",
        "GiB",
        "TiB",
        "PiB",
        "EiB",
        "ZiB",
        "YiB",
    ];
    for (
        nMultiple = 0, nApprox = nBytes / 1024;
        nApprox > 1;
        nApprox /= 1024, nMultiple++
    ) {
        sOutput =
            nApprox.toFixed(3) +
            " " +
            aMultiples[nMultiple] +
            " (" +
            nBytes +
            " bytes)";
    }

    // end of optional code
    document.getElementById("fileNum").innerHTML = nFiles;
    document.getElementById("fileSize").innerHTML = sOutput;

    console.log(oFiles)
    console.log(fileNames);
    for (let file of fileNames) {
        document.getElementById("myfiles").innerHTML += `<span>${file}</span><br>`;

    }
}

document.getElementById("uploadInput").addEventListener("change", updateSize);