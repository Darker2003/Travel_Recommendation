
const Item = ({ item }) => {
    console.log(item)
    return (
        <>
            <div className="mb-8">
                <div className="h-60 w-full ">
                    {/* Ensure the 'object-cover' class maintains aspect ratio */}
                    <img className="object-cover h-full w-full" src={item.image} alt={item.name} />
                </div>

                <div className="mb-4">{item.name}</div>
                <div className="max-h-40 overflow-y-auto">{item.description}</div>
            </div>
        </>
    )
}

export default Item