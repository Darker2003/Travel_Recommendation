import { useEffect, useState } from "react"
import { fetchData } from "../../../apis/Api"
import Item from "./item"

const Destination = () => {
  const [data, setData] = useState([])
  const fecth = async () => {
    const data = await fetchData()
    setData(data)
    console.log(data)
  }
  useEffect(() => {

    fecth()
  }, [])
  return (
    <>
      <div>Destination</div>
      <div className="grid gap-8 grid-cols-5 mt-4">
        {data.map((item, index) => <Item key={index} item={item} />)}
        
      </div>
    </>

  )
}

export default Destination