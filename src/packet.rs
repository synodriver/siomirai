use pyo3::prelude::*;
use rq_engine::hex::encode_hex;
use rq_engine::protocol::packet::{EncryptType, Packet, PacketType};

use crate::pbytes::PBytes;

#[pyclass(name = "Packet")]
#[derive(Default, Clone)]
pub struct PyPacket {
    #[pyo3(get, set)]
    pub packet_type: u32,
    #[pyo3(get, set)]
    pub encrypt_type: u32,
    #[pyo3(get, set)]
    pub seq_id: i32,
    #[pyo3(get, set)]
    pub body: PBytes,
    #[pyo3(get, set)]
    pub command_name: String,
    #[pyo3(get, set)]
    pub uin: i64,
    #[pyo3(get, set)]
    pub message: String,
}

#[pymethods]
impl PyPacket {
    #[new]
    fn new() -> Self {
        Self::default()
    }

    fn __str__(&self) -> String {
        format!("<Packet seq_id={}, command_name={}, body={}>", self.seq_id, self.command_name,encode_hex(&self.body.0))
    }
}

impl From<Packet> for PyPacket {
    fn from(p: Packet) -> Self {
        Self {
            packet_type: p.packet_type.value(),
            encrypt_type: p.encrypt_type.value(),
            seq_id: p.seq_id,
            body: PBytes(p.body),
            command_name: p.command_name,
            uin: p.uin,
            message: p.message,
        }
    }
}

impl From<PyPacket> for Packet {
    fn from(p: PyPacket) -> Self {
        Self {
            packet_type: PacketType::from_i32(p.packet_type as i32).unwrap(),
            encrypt_type: EncryptType::from_u8(p.encrypt_type as u8).unwrap(),
            seq_id: p.seq_id,
            body: p.body.0,
            command_name: p.command_name,
            uin: p.uin,
            message: p.message,
        }
    }
}