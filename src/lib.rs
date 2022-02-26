use pyo3::prelude::*;

use device::PyDevice;
use packet::PyPacket;
// use transport::PyTransport;
use engine::*;

pub mod device;
pub mod transport;
pub mod packet;
pub mod pbytes;
pub mod engine;

/// A Mirai Protocol Parser.
#[pymodule]
fn _rqpy(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyDevice>()?;
    m.add_class::<PyPacket>()?;
    // m.add_class::<PyTransport>()?;
    m.add_class::<PyEngine>()?;
    m.add_class::<PyLoginResponse>()?;
    m.add_class::<PyLoginSuccess>()?;
    m.add_class::<PyAccountInfo>()?;
    m.add_class::<PyQRCodeState>()?;
    m.add_class::<PyQRCodeConfirmed>()?;
    m.add_class::<PyQRCodeImageFetch>()?;
    m.add_class::<PyLoginDeviceLocked>()?;
    m.add_class::<PyLoginNeedCaptcha>()?;
    Ok(())
}