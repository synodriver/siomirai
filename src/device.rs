use pyo3::prelude::*;
use rq_engine::protocol::device::Device;

#[pyclass(name="Device")]
#[derive(Clone)]
pub struct PyDevice {
    pub inner: Device,
}

#[pymethods]
impl PyDevice {
    #[staticmethod]
    fn random() -> PyResult<Self> {
        Ok(Self{inner:Device::random()})
    }

    fn __str__(&self)->PyResult<String>{
        Ok(serde_json::to_string(&self.inner).unwrap())
    }
}
