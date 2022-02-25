use pyo3::prelude::*;

use device::PyDevice;
use packet::PyPacket;
// use transport::PyTransport;
use engine::{PyEngine, PyLoginResponse, PyLoginSuccess, PyAccountInfo, PyQRCodeState, PyQRCodeConfirmed, PyQRCodeImageFetch};

pub mod device;
pub mod transport;
pub mod packet;
pub mod pbytes;
pub mod engine;

/// sum_as_string(a: int, b: int) -> str
/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Mirai Protocol Parser.
#[pymodule]
fn siomirai(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
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
    Ok(())
}