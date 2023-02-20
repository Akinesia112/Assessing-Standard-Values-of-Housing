let map;

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
      // 中心點位置
      center: { lat: 23.05, lng: 120.30 }, 

      zoom: 11, // 地圖縮放比例 (0-20)
      maxZoom: 20, // 使用者能縮放地圖的最大比例 
      minZoom: 10, // 使用者能縮放地圖的最小比例
      
      streetViewControl: false, // 是否顯示右下角街景小人
      mapTypeControl: false // 使用者能否切換地圖樣式：一般、衛星圖等
    });
  }

