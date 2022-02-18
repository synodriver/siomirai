use pyo3::prelude::*;

use device::PyDevice;
use packet::PyPacket;
// use transport::PyTransport;
use engine::PyEngine;

pub mod device;
pub mod transport;
pub mod packet;
pub mod pbytes;
pub mod engine;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Mirai Protocol Parser.
#[pymodule]
fn _rqpy(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_class::<PyDevice>()?;
    m.add_class::<PyPacket>()?;
    // m.add_class::<PyTransport>()?;
    m.add_class::<PyEngine>()?;
    Ok(())
}