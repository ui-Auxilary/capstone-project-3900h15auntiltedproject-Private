import { useCallback, useState } from "react";
import { FileRejection, useDropzone } from "react-dropzone";

import File from "assets/upload_file.svg"

import S from "./style"

export default function Dropzone() {
  const [files, setFiles] = useState<File[]>([]);
  const [rejectedfiles, setRejectedFiles] = useState<FileRejection[]>([]);

  const onDrop = useCallback(
    (acceptedFiles: File[], fileRejections: FileRejection[]) => {
      if (acceptedFiles?.length) {
        setFiles((previousFiles) => [...previousFiles, ...acceptedFiles]);
      }

      if (fileRejections?.length) {
        setRejectedFiles((previousFiles) => [
          ...previousFiles,
          ...fileRejections,
        ]);
      }
    },
    [],
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      "text/x-python": [".py"],
    },
    onDrop,
  });

  const fileDisplay = files?.map((file) => (
    <S.FileBox key={window.crypto.randomUUID()}>
      <S.FileIcon style={{ width: "12%", marginRight: "5px", marginTop: "-10px" }} src={File} />
      <p><strong>{file.name}</strong><br /><span style={{ color: "#aaa" }}>{file.size} bytes</span></p>
    </S.FileBox>
  ));

  return (
    <>
      <S.Container
        style={{ background: isDragActive ? "#ededed" : "#FFE3E3" }}
        {...getRootProps()}
      >
        <input {...getInputProps()} />
        <S.Wrapper>
          <S.FileIcon src={File} />
          <h6>Drag & Drop or <div style={{ cursor: "pointer", color: "#5f7cce", textAlign: "center" }}><strong>browse</strong></div></h6>
        </S.Wrapper>
      </S.Container>
      <aside>

        {fileDisplay.length > 0 ? (<S.ScrollableDiv>
          {fileDisplay}
        </S.ScrollableDiv>) : null}

        {/* <h4>Rejected files</h4>
        {rejectedfiles &&
          rejectedfiles.map((file) =>
            file.errors.map((error) => (
              <ul>
                {error.code} {error.message}
              </ul>
            )),
          )} */}
      </aside>
    </>
  );
}
