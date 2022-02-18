// use pyo3::prelude::*;
// use rq_engine::protocol::packet::Packet;
// use rq_engine::protocol::transport::Transport;
// use rq_engine::protocol::version::{get_version, Protocol};
//
// use crate::device::PyDevice;
// use crate::packet::PyPacket;
// use crate::pbytes::PBytes;
//
// #[pyclass(name="Transport")]
// pub struct PyTransport {
//     pub inner: Transport,
// }
//
// #[pymethods]
// impl PyTransport {
//     #[new]
//     fn new(device: PyDevice, protocol: i32) -> Self {
//         let protocol = match protocol {
//             1 => Protocol::AndroidPhone,
//             2 => Protocol::AndroidWatch,
//             3 => Protocol::MacOS,
//             4 => Protocol::QiDian,
//             _ => Protocol::IPad
//         };
//         Self {
//             inner: Transport::new(device.inner, get_version(protocol))
//         }
//     }
//
//     fn decode_packet(&self, payload: &[u8]) -> PyPacket {
//         let pkt = self.inner.decode_packet(payload).unwrap();
//         PyPacket::from(pkt)
//     }
//
//     fn encode_packet(&self, pkt: PyPacket) -> PBytes {
//         let b = self.inner.encode_packet(Packet::from(pkt));
//         PBytes(b)
//     }
// }