import PageTemplate from "components/PageTemplate/PageTemplate";
import DragAndDrop from "components/DragAndDrop";

import Button from "react-bootstrap/Button";

import Sidebar from "../../components/Sidebar";
import S from "./style";

import ChartComponent from "components/Visualization/Visualization";
import { useEffect, useState } from "react";
import PipeList from "components/PipeList/PipeList";
import FormProvider from "components/Form/FormProvider";
import { useAppData } from "helper/AppProvider";
import getUser from "helper/functions";

export default function Home() {
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  if (sessionStorage.getItem("token") === null) {
    window.location.href = "/login";
  }

  const { user, setUser } = useAppData()

  useEffect(() => {
    getUser().then(({ user }) => setUser(user.id))

  }, [])

  return (
    <PageTemplate>
      <S.Wrapper>
        <Sidebar />
        <S.Container>
          <S.Header>
            <div style={{ display: "flex", gap: "25px" }}>
              <h3>Pipeline</h3>
              <Button onClick={handleShow}>+ Create pipeline</Button>
            </div>
            <span>Create a pipeline</span>
          </S.Header>
          <S.Body>
            <PipeList />
          </S.Body>
        </S.Container>
      </S.Wrapper>
      <FormProvider>
        <DragAndDrop show={show} handleClose={handleClose} />
      </FormProvider>
    </PageTemplate>
  );
}
