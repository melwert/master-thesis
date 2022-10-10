export const state = () => ({
    currentProject: "NoneStore",
    currentProjectId: "",
    currentPerson: "NoneStore",
    currentPersonId: "",
  })
  
  export const getter = {
    getCurrentProject(state) {
      return state.currentProject
    },
    getCurrentProjectId(state) {
        return state.currentProjectId
    },
    getCurrentPerson(state) {
      return state.currentPerson
    },
    getCurrentPersonId(state) {
        return state.currentPersonId
    }
  }
  
  export const mutations = {
    setCurrentProject(state, newCurrentProject) {
      state.currentProject = newCurrentProject
    },
    setCurrentProjectId(state, newCurrentProjectId) {
        state.currentProjectId = newCurrentProjectId
    },
    setCurrentPerson(state, newCurrentPerson) {
      state.currentPerson = newCurrentPerson
    },
    setCurrentPersonId(state, newCurrentPersonId) {
        state.currentPersonId = newCurrentPersonId
    }
  }
  
//   export const actions = {
//     async fetchCounter(state) {
//       // make request
//       const res = { data: 10 };
//       state.counter = res.data;
//       return res.data;
//     }
//   }
  