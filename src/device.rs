use pyo3::prelude::*;
use rq_engine::protocol::device::Device;
use crate::pbytes::PBytes;

/// The Device
#[pyclass(name = "Device")]
#[derive(Clone)]
pub struct PyDevice {
    pub inner: Device,
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
           imei: String) -> PyDevice {
        return PyDevice {
            inner: Device {
                display,
                product,
                device,
                board,
                model,
                finger_print,
                boot_id,
                proc_version,
                imei,
                brand: "".to_string(),
                bootloader: "".to_string(),
                base_band: "".to_string(),
                version: Default::default(),
                sim_info: "".to_string(),
                os_type: "".to_string(),
                mac_address: "".to_string(),
                ip_address: vec![],
                wifi_bssid: "".to_string(),
                wifi_ssid: "".to_string(),
                imsi_md5: vec![],
                android_id: "".to_string(),
                apn: "".to_string(),
                vendor_name: "".to_string(),
                vendor_os_name: "".to_string(),
            }
        };
    }
    /// random() -> Device
    /// --
    ///
    /// Generate random device
    #[staticmethod]
    fn random() -> PyResult<Self> {
        Ok(Self { inner: Device::random() })
    }

    /// ksid(self) -> bytes
    /// --
    ///
    /// get ksid
    fn ksid(&self) -> PBytes {
        let data = self.inner.ksid();
        return PBytes(data);
    }

    fn __str__(&self) -> PyResult<String> {
        Ok(serde_json::to_string(&self.inner).unwrap())
    }
}
