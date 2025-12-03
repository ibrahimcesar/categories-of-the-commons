import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import ExplorePage from './pages/ExplorePage'
import EquationsPage from './pages/EquationsPage'
import ComparePage from './pages/ComparePage'
import ContributePage from './pages/ContributePage'
import ProjectPage from './pages/ProjectPage'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/explore" element={<ExplorePage />} />
        <Route path="/equations" element={<EquationsPage />} />
        <Route path="/compare" element={<ComparePage />} />
        <Route path="/contribute" element={<ContributePage />} />
        <Route path="/project/:owner/:repo" element={<ProjectPage />} />
      </Routes>
    </Layout>
  )
}

export default App
