document.addEventListener("DOMContentLoaded", async function () {
  await fetchData();
  await fetchBME();
  setInterval(fetchData, 10000);
});

// Fungsi fetch data
async function fetchData() {
  try {
    const response = await fetch('/api/tanaman');
    const data = await response.json();

    const dataList = document.getElementById("data-list");
    dataList.innerHTML = "";

    data.forEach(item => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${item.jenis_zona}</td>
        <td>${item.nama}</td>
        <td>${item.keterangan}</td>
        <td>${item.latin}</td>
        <td>${item.suhu_optimal}</td>
        <td>${item.kelembaban_optimal}</td>
      `;
      dataList.appendChild(row);
    });
  } catch (error) {
    console.error("Error:", error);
  }
}

async function fetchBME() {
  try {
    const response = await fetch('/api/bme');
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log("Received data:", data);
    
    // Update data sensor
    document.getElementById("bme-temperature").innerText = data.temperature;
    document.getElementById("bme-pressure").innerText = data.pressure;
    document.getElementById("bme-altitude").innerText = data.altitude;
    document.getElementById("zoneName").textContent = data.zone || "Unknown";
    
  } catch (error) {
    console.error("❌ Error fetching BME data:", error);
    
    // Set default values jika error
    document.getElementById("bme-temperature").innerText = "Error";
    document.getElementById("bme-pressure").innerText = "Error";
    document.getElementById("bme-altitude").innerText = "Error";
    document.getElementById("zoneName").textContent = "Connection Error";
  }
}
