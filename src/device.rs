use pyo3::prelude::*;
use rq_engine::protocol::device::Device;
use crate::pbytes::PBytes;

/// The Device
#[pyclass(name="Device")]
#[derive(Clone)]
pub struct PyDevice {
    pub inner: Device,
}

#[pymethods]
impl PyDevice {
    /// random() -> Device
    /// --
    ///
    /// Generate random device
    #[staticmethod]
    fn random() -> PyResult<Self> {
        Ok(Self{inner:Device::random()})
    }

    /// ksid(self) -> bytes
    /// --
    ///
    /// get ksid
    fn ksid(&self) -> PBytes {
        let data = self.inner.ksid();
        return PBytes(data);
    }

    fn __str__(&self)->PyResult<String>{
        Ok(serde_json::to_string(&self.inner).unwrap())
    }
}
