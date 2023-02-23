import "../../Style/ImageList.css"
import {useEffect, useState} from "react";

const ImageList = ({userName}) => {
    const [images, setImages] = useState(null)
    const [targetImage, setTargetImage] = useState(null)
    const [listItems, setListItems] = useState(null)

    useEffect(() => {
        getImages();
    }, []);
    
    const getImages = async () => {
        let owner = "test"
        
        await fetch(`http://localhost:8080/files`)
        .then(x => x.json())
        .then(x =>
        {
            console.log(x)
            setImages(x)
            setListItems(createList())
        })
    }
    
    const handleTargetImage = event => {
        setTargetImage(event.target.files[0])
    }

    const uploadImage = async event => {
        event.preventDefault()
        
        const formData = new FormData()
        formData.append('image', targetImage)

        await fetch('https://localhost:7011/Image/upload', {
            method: 'POST',
            mode: 'cors',
            body: formData
        })
            .then(x => x.text())
            .then(x => {console.log(x)})

        await getImages()
    }
    
    const deleteImage = async (id) => {
        await fetch(`https://localhost:7011/Image/delete?id=${id}`)

        await getImages()
    }

    const downloadImage = async (id, name) => {
        console.log(id)
        const response = await fetch(`https://localhost:7011/Image/download?id=${id}`)

        console.log(response.headers)
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = name + '.jpeg';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        } 
        else {
            console.log(`Error downloading image: ${response.status} ${response.statusText}`);
        }
    }
    
    const createList = () => {
        return (
            <div className="image-list">
                {images.map((image, id) => (
                    <div className = "image-grid">
                        <div className ="description-name">{image.name}</div>
                        <div className ="description-size">{image.size} kb</div>
                        <button className="button" onClick={() => downloadImage(image.id, image.name)}>DOWNLOAD</button>
                        <button className="button" onClick={() => deleteImage(image.id)}>DELETE</button>
                    </div>
                ))}
            </div>
        );
    };

    return (
        <div className="main-container">
            
            <div className="image-container">
                {listItems}
            </div>
            
            <br></br>
            
            <form className="upload-container" onSubmit={uploadImage}>
                <input type="file" onChange={handleTargetImage}/>
                <button type="submit">Upload</button>
            </form>

            <br></br>

            <div className="upload-container">
                <button className="update" onClick={() => getImages()}>UPDATE</button>
            </div>

            <br></br>

        </div>

    );
}
export default ImageList;
