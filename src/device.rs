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
           imei: String,
           brand: String,
           bootloader: String,
           base_band: String,
           // version: String,
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
    ) -> PyDevice {
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
                brand,
                bootloader,
                base_band,
                version: Default::default(),
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
