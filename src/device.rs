use pyo3::prelude::*;
use rq_engine::protocol::device::{Device, OSVersion};
use crate::pbytes::PBytes;

/// The Device
#[pyclass(name = "Device")]
#[derive(Clone)]
pub struct PyDevice {
    #[pyo3(get, set)]
    pub display: String,
    #[pyo3(get, set)]
    pub product: String,
    #[pyo3(get, set)]
    pub device: String,
    #[pyo3(get, set)]
    pub board: String,
    #[pyo3(get, set)]
    pub model: String,
    #[pyo3(get, set)]
    pub finger_print: String,
    #[pyo3(get, set)]
    pub boot_id: String,
    #[pyo3(get, set)]
    pub proc_version: String,
    #[pyo3(get, set)]
    pub imei: String,
    #[pyo3(get, set)]
    pub brand: String,
    #[pyo3(get, set)]
    pub bootloader: String,
    #[pyo3(get, set)]
    pub base_band: String,
    #[pyo3(get, set)]
    pub version: PyOSVersion,
    #[pyo3(get, set)]
    pub sim_info: String,
    #[pyo3(get, set)]
    pub os_type: String,
    #[pyo3(get, set)]
    pub mac_address: String,
    #[pyo3(get, set)]
    pub ip_address: Vec<u8>,
    #[pyo3(get, set)]
    pub wifi_bssid: String,
    #[pyo3(get, set)]
    pub wifi_ssid: String,
    #[pyo3(get, set)]
    pub imsi_md5: Vec<u8>,
    #[pyo3(get, set)]
    pub android_id: String,
    #[pyo3(get, set)]
    pub apn: String,
    #[pyo3(get, set)]
    pub vendor_name: String,
    #[pyo3(get, set)]
    pub vendor_os_name: String,
}

impl From<Device> for PyDevice {
    fn from(d: Device) -> Self {
        Self {
            display: d.display,
            product: d.product,
            device: d.device,
            board: d.board,
            model: d.model,
            finger_print: d.finger_print,
            boot_id: d.boot_id,
            proc_version: d.proc_version,
            imei: d.imei,
            brand: d.brand,
            bootloader: d.bootloader,
            base_band: d.base_band,
            version: d.version.into(),
            sim_info: d.sim_info,
            os_type: d.os_type,
            mac_address: d.mac_address,
            ip_address: d.ip_address,
            wifi_bssid: d.wifi_bssid,
            wifi_ssid: d.wifi_ssid,
            imsi_md5: d.imsi_md5,
            android_id: d.android_id,
            apn: d.apn,
            vendor_name: d.vendor_name,
            vendor_os_name: d.vendor_os_name,
        }
    }
}

impl From<PyDevice> for Device {
    fn from(d: PyDevice) -> Self {
        Self {
            display: d.display,
            product: d.product,
            device: d.device,
            board: d.board,
            model: d.model,
            finger_print: d.finger_print,
            boot_id: d.boot_id,
            proc_version: d.proc_version,
            imei: d.imei,
            brand: d.brand,
            bootloader: d.bootloader,
            base_band: d.base_band,
            version: d.version.into(),
            sim_info: d.sim_info,
            os_type: d.os_type,
            mac_address: d.mac_address,
            ip_address: d.ip_address,
            wifi_bssid: d.wifi_bssid,
            wifi_ssid: d.wifi_ssid,
            imsi_md5: d.imsi_md5,
            android_id: d.android_id,
            apn: d.apn,
            vendor_name: d.vendor_name,
            vendor_os_name: d.vendor_os_name,
        }
    }
}

impl From<&PyDevice> for Device {
    fn from(d: &PyDevice) -> Self {
        Self {
            display: d.display.clone(),
            product: d.product.clone(),
            device: d.device.clone(),
            board: d.board.clone(),
            model: d.model.clone(),
            finger_print: d.finger_print.clone(),
            boot_id: d.boot_id.clone(),
            proc_version: d.proc_version.clone(),
            imei: d.imei.clone(),
            brand: d.brand.clone(),
            bootloader: d.bootloader.clone(),
            base_band: d.base_band.clone(),
            version: d.version.clone().into(),
            sim_info: d.sim_info.clone(),
            os_type: d.os_type.clone(),
            mac_address: d.mac_address.clone(),
            ip_address: d.ip_address.clone(),
            wifi_bssid: d.wifi_bssid.clone(),
            wifi_ssid: d.wifi_ssid.clone(),
            imsi_md5: d.imsi_md5.clone(),
            android_id: d.android_id.clone(),
            apn: d.apn.clone(),
            vendor_name: d.vendor_name.clone(),
            vendor_os_name: d.vendor_os_name.clone(),
        }
    }
}

#[pyclass(name = "OSVersion")]
#[derive(Clone)]
pub struct PyOSVersion {
    #[pyo3(get, set)]
    pub incremental: String,
    #[pyo3(get, set)]
    pub release: String,
    #[pyo3(get, set)]
    pub codename: String,
    #[pyo3(get, set)]
    pub sdk: u32,
}

impl From<OSVersion> for PyOSVersion {
    fn from(v: OSVersion) -> Self {
        Self {
            incremental: v.incremental,
            release: v.release,
            codename: v.codename,
            sdk: v.sdk,
        }
    }
}

impl From<PyOSVersion> for OSVersion {
    fn from(v: PyOSVersion) -> Self {
        Self {
            incremental: v.incremental,
            release: v.release,
            codename: v.codename,
            sdk: v.sdk,
        }
    }
}


#[pymethods]
impl PyDevice {
    #[new]
    fn new(display: String,
           product: String,
           device: String,
           board: String,
           model: String,
           finger_print: String,
           boot_id: String,
           proc_version: String,
           imei: String,
           brand: String,
           bootloader: String,
           base_band: String,
           version: PyOSVersion,
           sim_info: String,
           os_type: String,
           mac_address: String,
           ip_address: &[u8],
           wifi_bssid: String,
           wifi_ssid: String,
           imsi_md5: &[u8],
           android_id: String,
           apn: String,
           vendor_name: String,
           vendor_os_name: String,
    ) -> Self
    {
        return Self {
            display,
            product,
            device,
            board,
            model,
            finger_print,
            boot_id,
            proc_version,
            imei,
            brand,
            bootloader,
            base_band,
            version,
            sim_info,
            os_type,
            mac_address,
            ip_address: ip_address.to_vec(),
            wifi_bssid,
            wifi_ssid,
            imsi_md5: imsi_md5.to_vec(),
            android_id,
            apn,
            vendor_name,
            vendor_os_name,
        };
    }
    /// random() -> Device
    /// --
    ///
    /// Generate random device
    #[staticmethod]
    fn random() -> PyResult<Self> {
        Ok(Device::random().into())
    }

    /// ksid(self) -> bytes
    /// --
    ///
    /// get ksid
    fn ksid(&self) -> PBytes {
        let device = Device::from(self);
        return PBytes(device.ksid());
    }

    fn __str__(&self) -> PyResult<String> {
        Ok(serde_json::to_string(&Device::from(self.clone())).unwrap())
    }
}
